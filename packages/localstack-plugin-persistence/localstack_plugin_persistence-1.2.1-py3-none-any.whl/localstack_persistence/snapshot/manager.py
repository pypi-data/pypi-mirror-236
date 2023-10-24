_B=True
_A=False
import logging,os.path,threading,time
from typing import Dict,Set
from localstack.aws.api import RequestContext
from localstack.config import SNAPSHOT_FLUSH_INTERVAL
from localstack.services.plugins import ServiceManager
from localstack.state import StateVisitor
from localstack.state.snapshot import SnapshotPersistencePlugin
from localstack.utils.json import FileMappedDocument
from localstack.utils.scheduler import Scheduler
from localstack.utils.sync import SynchronizedDefaultDict
from plugin import PluginManager
from readerwriterlock import rwlock
from localstack_persistence import constants
from..manager import StateManager
from..utils import DefaultPrioritySorter,ServiceSorter
from.load import LoadSnapshotVisitor
from.save import SaveSnapshotVisitor
LOG=logging.getLogger(__name__)
class SnapshotManager(StateManager):
	'\n    This implements the glue for making the simple disk-based persistence strategy work. It instantiates\n    the correct visitors, uses a ``ServiceManager`` to locate service plugins, and makes sure\n    ``StateLifecycleHook``s are invoked appropriately.\n    ';service_manager:0;data_dir:0;persistence_plugin_manager:0;service_sorter:0
	def __init__(A,service_manager,data_dir,service_sorter=None):B=data_dir;super().__init__(service_manager);A.data_dir=B;A.tracker=FileMappedDocument(os.path.join(B,constants.API_STATES_JSON));A.persistence_plugin_manager=PluginManager(SnapshotPersistencePlugin.namespace);A.service_sorter=service_sorter or DefaultPrioritySorter()
	def load(C,service_name,visitor=None):B=service_name;A=visitor;A=A or C._create_load_state_visitor(B);super().load(B,A)
	def save(A,service_name,visitor=None):C=visitor;B=service_name;C=C or A._create_save_state_visitor(B);A.tracker[B]=time.time();A.tracker.save();super().save(B,C)
	def save_all(A):
		'\n        Saves the state of all loaded services.\n        '
		for B in A.service_manager.values():C=A._create_save_state_visitor(B.name());A.save(service_name=B,visitor=C)
	def load_all(A):
		'\n        Loads the state of all services that are found in the tracker file.\n        '
		for B in A.service_sorter.sort_services(list(A.tracker.keys())):C=A._create_save_state_visitor(B);A.load(service_name=B,visitor=C)
	def _create_load_state_visitor(A,service_name):
		'\n        Creates a ``StateVisitor`` for loading the state of a service.\n        :param service_name: the service\n        :return: an instance of LoadSnapshotVisitor\n        ';B=service_name
		if A.persistence_plugin_manager.exists(B):
			D=A.persistence_plugin_manager.load(B);C=D.create_load_snapshot_visitor(B,A.data_dir)
			if C:return C
		return LoadSnapshotVisitor(B,data_dir=A.data_dir)
	def _create_save_state_visitor(A,service_name):
		'\n        Creates a ``StateVisitor`` for saving the state of a service.\n        :param service_name: the service\n        :return: an instance of SaveSnapshotVisitor\n        ';B=service_name
		if A.persistence_plugin_manager.exists(B):
			D=A.persistence_plugin_manager.load(B);C=D.create_save_snapshot_visitor(B,A.data_dir)
			if C:return C
		return SaveSnapshotVisitor(B,A.data_dir)
class LoadOnRequestHandler:
	'\n    Facilitates the "ON_REQUEST" load strategy.\n    ';state_manager:0
	def __init__(A,state_manager):A.state_manager=state_manager;A._locks=SynchronizedDefaultDict(threading.RLock);A._restored=set()
	def on_request(B,_chain,context,_response):
		C=context
		if not C.service:return
		A=C.service.service_name
		if A in B._restored:return
		if not B._locks[A].acquire(timeout=10):LOG.debug('skipping state load, service %s may still be loading state %s ',A);return
		try:
			if A in B._restored:return
			try:B.state_manager.load(A)
			finally:B._restored.add(A)
		finally:B._locks[A].release()
def _should_save_request(context):
	'\n    This method determines whether a particular AWS request should trigger a state save.\n    :param context: the request context\n    :return:\n    ';A=context
	if getattr(A,'_skip_snapshot_save',_A):return _A
	if not A.service:return _A
	if A.request.method not in['POST','PUT','PATCH','DELETE']:return _A
	if A.operation:
		B=A.operation.name
		if B.startswith('List')or B.startswith('Get')or B.startswith('Describe'):return _A
	elif A.service.service_name=='s3':return _A
	return _B
class SaveOnRequestHandler:
	'\n    Facilitates the "ON_REQUEST" save strategy.\n    ';state_manager:0
	def __init__(A,state_manager):A.state_manager=state_manager;A._locks=SynchronizedDefaultDict(threading.RLock)
	def on_request(C,_chain,context,_response):
		A=context
		if not _should_save_request(A):return
		B=A.service.service_name
		if not C._locks[B].acquire(timeout=5):LOG.debug('skipping state save, service %s may still be saving state',B);A._skip_snapshot_save=_B
		else:A._skip_snapshot_save=_A
	def on_response(A,_chain,context,_response):
		B=context
		if not _should_save_request(B):return
		C=B.service.service_name;D=A._locks[C]
		try:A.state_manager.save(C)
		finally:D.release()
class SaveStateScheduler:
	'\n    Saves the state on a regular basis, and facilitates the "SCHEDULED" save strategy (a compromise between\n    ON_REQUEST and ON_SHUTDOWN).\n\n    It also exposes a Handler that should be added to the handler chain, which schedules services similar\n    to the SaveOnRequestHandler.\n    ';state_manager:0;period:0
	def __init__(A,state_manager,period=SNAPSHOT_FLUSH_INTERVAL):A.state_manager=state_manager;A.scheduler=Scheduler();A.period=period;A._dirty_markers=set();A._marker_lock=threading.Lock();A._save_lock=rwlock.RWLockWrite()
	def start(A):threading.Thread(target=A.scheduler.run,daemon=_B).start();A.scheduler.schedule(A._do_save,period=A.period)
	def schedule_for_save(A,service):
		'\n        Schedule the given service into the next save cycle. Call this when you think the state of a\n        service may have changed and should be flushed to disk.\n\n        :param service: the service to be stored\n        '
		with A._marker_lock:A._dirty_markers.add(service)
	def _do_save(A):
		'\n        Internal routine to perform save calls through the StateManager.\n        ';C=time.perf_counter()
		with A._marker_lock:
			B=list(A._dirty_markers);A._dirty_markers.clear()
			if not B:return
		with A._save_lock.gen_wlock():
			LOG.debug('Saving snapshot for services %s',B)
			for D in B:A.state_manager.save(D)
		LOG.info('Saving snapshot to disk took %.2f seconds',time.perf_counter()-C)
	def close(A):A.scheduler.close();A._do_save()
	def on_request(B,_chain,context,_response):
		A=context
		if not _should_save_request(A):return
		B.schedule_for_save(A.service.service_name);A._snapshot_save_rlock=B._save_lock.gen_rlock()
		if not A._snapshot_save_rlock.acquire(timeout=10):LOG.warning('waiting on snapshot save timed out, this can cause data corruption');A._skip_snapshot_save=_B
		else:A._skip_snapshot_save=_A
	def on_response(B,_chain,context,_response):
		A=context
		if not _should_save_request(A):return
		A._snapshot_save_rlock.release()