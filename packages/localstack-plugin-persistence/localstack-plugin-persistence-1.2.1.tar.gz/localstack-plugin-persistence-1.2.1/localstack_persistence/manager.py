import logging
from localstack.services.plugins import ServiceManager
from localstack.state import StateVisitor
from localstack.utils.functions import call_safe
LOG=logging.getLogger(__name__)
class StateManager:
	service_manager:0;'Handles service plugins.'
	def __init__(A,service_manager):A.service_manager=service_manager
	def save(C,service_name,visitor=None):
		'\n        Saves the state of a service. The saving logic is handled by the visitor.\n        :param service_name: the name of the service to save\n        :param visitor: the visitor that handles the saving logic\n        ';B=service_name
		if(A:=C.service_manager.get_service(B)):call_safe(A.lifecycle_hook.on_before_state_save);LOG.debug('Serializing state of service %s',B);A.accept_state_visitor(visitor);call_safe(A.lifecycle_hook.on_after_state_save)
	def load(C,service_name,visitor=None):
		'\n        Loads the state of a service. The loading logic is handled by the visitor.\n        :param service_name: the name of the service to load\n        :param visitor: the visitor that handles the loading logic\n        ';B=service_name
		if(A:=C.service_manager.get_service(B)):call_safe(A.lifecycle_hook.on_before_state_load);LOG.debug('Loading state of service %s',B);A.accept_state_visitor(visitor);call_safe(A.lifecycle_hook.on_after_state_load)