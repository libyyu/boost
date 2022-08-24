try:
  __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
  __path__ = __import__('pkgutil').extend_path(__path__, __name__)


try:
  from google.protobuf import descriptor_pb2
except:
  descriptor_pb2.FixRegisterMessageSourceCodeInfo()
  descriptor_pb2.FixRegisterMessageGeneratedCodeInfo()