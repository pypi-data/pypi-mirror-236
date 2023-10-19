#  Copyright 2020-2023 Robert Bosch GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# *******************************************************************************
#
# File: dbus_manager.py
#
# Initially created by Nguyen Huynh Tri Cuong (MS/EMC12-XC) / May 2023.
#
# Description:
#   Provide a class to manage all DBus connections.
#
# History:
#
# 22.05.2023 / V 0.1.0 / Nguyen Huynh Tri Cuong
# - Initialize
#
# *******************************************************************************
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from RobotFramework_DBus.dbus_client import DBusClient
from RobotFramework_DBus.dbus_client_remote import DBusClientRemote
from RobotFramework_DBus.common.utils import Singleton
import threading
import platform
if platform.system().lower().startswith("linux"):
   from dasbus.connection import SessionMessageBus
   from dasbus.identifier import DBusServiceIdentifier, DBusObjectIdentifier
   from dasbus.client.proxy import disconnect_proxy
   from dasbus.client.observer import DBusObserver
   from dasbus.loop import EventLoop


class DBusManager(Singleton):
   """
Class to manage all DBus connections.
   """
   ROBOT_LIBRARY_SCOPE = 'GLOBAL'
   ROBOT_AUTO_KEYWORDS = False

   ERR_CONNECTION_NAME_EXIST_STR = "The connection name '%s' has already existed! Please use other name"
   ERR_UNNABLE_CREATE_CONNECTION_STR = "Unable to create connection. Exception: %s"
   ERR_SET_SIGNAL_HANDLER_STR = "Unable to set '%s' keyword as handler for '%s' signal. Exception: %s"
   ERR_UNSET_SIGNAL_HANDLER_STR = "Unable to unset '%s' keyword as handler for '%s' signal. Exception: %s"
   ERR_REGISTER_SIGNAL_STR = "Unable to register '%s' signal to monitoring list. Exception: %s"
   ERR_CALL_DBUS_METHOD_STR = "Problem occurs when calling '%s' method.  Exception: %s"
   ERR_WAIT_DBUS_SIGNAL_STR = "Problem occurs when waiting for '%s' signal.  Exception: %s"

   idx = 0

   def __init__(self):
      """
Constructor for DBusManager class.

**Returns:**

(*no returns*)
      """
      self.connection_manage_dict = {}

   def __del__(self):
      """
Destructor for ConnectionManager class.

**Returns:**

(*no returns*)
      """
      self.quit()

   def quit(self):
      """
Quit connection manager.

**Returns:**

(*no returns*)
      """
      for connection in self.connection_manage_dict.values():
         connection.quit()
      self.connection_manage_dict.clear()

   def add_connection(self, name, conn):
      """
Add a connection to managed dictionary.

**Arguments:**

* ``name``

  / *Condition*: required / *Type*: str /

  Connection's name.

* ``conn``

  / *Condition*: required / *Type*: DBusClient /

  Connection object.

**Returns:**

(*no returns*)
      """
      if name not in self.connection_manage_dict.keys():
         self.connection_manage_dict[name] = conn

   def remove_connection(self, connection_name):
      """
Remove a connection by name.

**Arguments:**

* ``connection_name``

  / *Condition*: required / *Type*: str /

  Connection's name.

**Returns:**

(*no returns*)
      """
      if connection_name in self.connection_manage_dict.keys():
         del self.connection_manage_dict[connection_name]


   def get_connection_by_name(self, connection_name):
      """
Get an exist connection by name.

**Arguments:**

* ``connection_name``

  / *Condition*: required / *Type*: str /

  Connection's name.

**Returns:**

* ``conn``

  / *Type*: socket.socket /

  Connection object.
      """
      conn = None
      if connection_name in self.connection_manage_dict.keys():
         conn = self.connection_manage_dict[connection_name]
      return conn

   @keyword
   def disconnect(self, connection_name):
      """
Keyword for disconnecting a connection by name.

**Arguments:**

* ``connection_name``

  / *Condition*: required / *Type*: str /

  Connection's name.

**Returns:**

(*no returns*)
      """
      if connection_name in self.connection_manage_dict.keys():
         self.connection_manage_dict[connection_name].quit()
         del self.connection_manage_dict[connection_name]
      elif connection_name.startswith("ALL"):
         self.connection_manage_dict.clear()

   @keyword
   def connect(self, conn_name='default_conn', namespace="", object_path=None, mode = "local", host="localhost", port=2507):
      """
Keyword used to establish a DBus connection.

**Arguments:**

* ``conn_name``

  / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

  The name or identifier of the connection instance used to interact with the DBus service.
  This parameter is optional and can be used to uniquely identify a specific connection
  when multiple connections are established. If not provided, a default connection will be used.

* ``namespace``

  / *Condition*: optional / *Type*: str / *Default*: '' /

  The namespace of the DBus service.
  This identifies the specific service or group of services.
  It is used to differentiate between different service instances.
  The namespace should be a string that uniquely identifies the service.

* ``object_path``

  / *Condition*: optional / *Type*: str / *Default*: None /

  The object path of the DBus service.
  This identifies the specific object within the service that the action will be performed on.
  The object path should be a string that follows the DBus object path naming convention.
  It typically consists of a hierarchical structure separated by slashes (/).

* ``mode``

  / *Condition*: optional / *Type*: str / *Default*: 'local' /

  The mode of testing the DBus service. Possible values are 'local' or 'remote'.
  'local' indicates testing on the current system, while 'remote' indicates testing on a remote system.

* ``host``

  / *Condition*: optional / *Type*: str / *Default*: 'localhost' /

  The IP address or hostname of the remote system where the DBus agent is running.

  This parameter is applicable only if `mode` is set to 'remote'.

* ``port``

  / *Condition*: optional / *Type*: int / *Default*: 2507 /

  The port number on which the DBus agent is listening on the remote system.

  This parameter is applicable only if `mode` is set to 'remote'.

**Returns:**

(*no returns*)
      """
      if conn_name in self.connection_manage_dict.keys():
         raise AssertionError(DBusManager.ERR_CONNECTION_NAME_EXIST_STR % conn_name)

      if conn_name == 'default_conn':
         conn_name += str(DBusManager.idx)
         DBusManager.idx += 1

      try:
         if mode == 'local':
            connection_obj = DBusClient(namespace, object_path)
         elif mode == 'remote':
            connection_obj = DBusClientRemote(namespace, object_path, host, int(port))
      except Exception as ex:
         # BuiltIn().log("Unable to create connection. Exception: %s" % ex, constants.LOG_LEVEL_ERROR)
         raise AssertionError("Unable to create connection. Exception: %s" % ex)

      if connection_obj is not None:
         setattr(connection_obj, 'connection_name', conn_name)
         if hasattr(connection_obj, "real_obj"):
            setattr(connection_obj.real_obj, 'connection_name', conn_name)
         self.add_connection(conn_name, connection_obj)

      try:
         connection_obj.connect()
      except Exception as ex:
         self.remove_connection(conn_name)
         # BuiltIn().log("Unable to create connection. Exception: %s" % ex, constants.LOG_LEVEL_ERROR)
         raise Exception(DBusManager.ERR_UNNABLE_CREATE_CONNECTION_STR % ex)

   @keyword
   def set_signal_received_handler(self, conn_name="", signal="", handler=None):
      """
Keyword used to set a signal received handler for a specific DBus connection and signal.

**Arguments:**

* ``conn_name``

  / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

  The name of the DBus connection.

* ``signal``

  / *Condition*: optional / *Type*: str / *Default*: '' /

  The name of the DBus signal to handle.

* ``handler``

  / *Condition*: optional / *Type*: str / *Default*: None /

  The keyword to handle the received signal.
  The handler should accept the necessary parameters based on the signal being handled.

**Returns:**

(*no returns*)
      """
      if conn_name not in self.connection_manage_dict.keys():
         raise AssertionError("The '%s' connection  hasn't been established. Please connect first." % conn_name)

      connection_obj = self.connection_manage_dict[conn_name]
      try:
         connection_obj.set_signal_received_handler(signal, handler)
      except Exception as ex:
         raise Exception(DBusManager.ERR_SET_SIGNAL_HANDLER_STR % (handler, signal, ex))

   @keyword
   def unset_signal_received_handler(self, conn_name="", signal="", handler=None):
      """
Keyword used to set a signal received handler for a specific DBus connection and signal.

**Arguments:**

* ``conn_name``

  / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

  The name of the DBus connection.

* ``signal``

  / *Condition*: optional / *Type*: str / *Default*: '' /

  The name of the DBus signal to handle.

* ``handler``

  / *Condition*: optional / *Type*: str / *Default*: None /

  The robotframework keyword which is handling the signal emitted event.

**Returns:**

(*no returns*)
      """
      if conn_name not in self.connection_manage_dict.keys():
         raise AssertionError("The '%s' connection  hasn't been established. Please connect first." % conn_name)

      connection_obj = self.connection_manage_dict[conn_name]
      try:
         connection_obj.unset_signal_received_handler(signal, handler)
      except Exception as ex:
         raise Exception(DBusManager.ERR_UNSET_SIGNAL_HANDLER_STR % (handler, signal, ex))

   @keyword
   def register_signal(self, conn_name="default_conn", signal=""):
      """
Keyword used to register a DBus signal or signals to be monitored for a specific connection.

**Arguments:**

* ``conn_name``

  / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

  The name of the DBus connection.

* ``signal``

  / *Condition*: optional / *Type*: str / *Default*: '' /

  The name of the DBus signal(s) to register. It can be a single signal name as a string,
  or multiple signal names joined by ','. For example: "signal1,signal2,signal3".

**Returns:**

(*no returns*)
      """
      if conn_name not in self.connection_manage_dict.keys():
         raise AssertionError("The '%s' connection  hasn't been established. Please connect first." % conn_name)

      connection_obj = self.connection_manage_dict[conn_name]
      try:
         connection_obj.register_monitored_signal(signal)
      except Exception as ex:
         raise Exception(DBusManager.ERR_REGISTER_SIGNAL_STR % (signal, ex))

   @keyword
   def call_dbus_method(self, conn_name="default_conn", method_name="", *args):
      """
Keyword used to call a DBus method with the specified method name and input arguments.

**Arguments:**

* ``conn_name``

  / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

  The name of the DBus connection.

* ``method_name``

  / *Condition*: optional / *Type*: str / *Default*: '' /

  The name of the DBus method to be called.

* ``args``

  / *Condition*: optional / *Type*: tuple / *Default*: None /

  Input arguments to be passed to the method.

**Returns:**

* ``ret_obj``

  / *Type*: Any /

  Return from called method.
      """
      if conn_name not in self.connection_manage_dict.keys():
         raise AssertionError("The '%s' connection  hasn't been established. Please connect first." % conn_name)

      ret_obj = None
      connection_obj = self.connection_manage_dict[conn_name]
      try:
         ret_obj = connection_obj.call_dbus_method(method_name, *args)
      except Exception as ex:
         raise Exception(DBusManager.ERR_CALL_DBUS_METHOD_STR % (method_name, ex))

      return ret_obj

#    @keyword
#    def call_dbus_method_with_keyword_args(self, conn_name="default_conn", method_name="", **kwargs):
#       """
# Keyword used to call a DBus method with the specified method name and input keyword arguments.

# **Arguments:**

# * ``conn_name``

#   / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

#   The name of the DBus connection.

# * ``method_name``

#   / *Condition*: optional / *Type*: str / *Default*: '' /

#   The name of the DBus method to be called.

# * ``kwargs``

#   / *Condition*: optional / *Type*: dict / *Default*: None /

#   Input keyword arguments to be passed to the method.

# **Returns:**

#   / *Type*: Any /

#   Return from called method.
#       """
#       if conn_name not in self.connection_manage_dict.keys():
#          raise AssertionError("The '%s' connection  hasn't been established. Please connect first." % conn_name)

#       ret_obj = None
#       connection_obj = self.connection_manage_dict[conn_name]
#       try:
#          ret_obj = connection_obj.call_dbus_method_with_keyword_args(method_name, **kwargs)
#       except Exception as ex:
#          raise Exception(DBusManager.ERR_CALL_DBUS_METHOD_STR % (method_name, ex))

#       return ret_obj

   @keyword
   def wait_for_signal(self, conn_name="default_conn", signal="", timeout=0):
      """
Keyword used to wait for a specific DBus signal to be received within a specified timeout period.

**Arguments:**

* ``conn_name``

  / *Condition*: optional / *Type*: str / *Default*: 'default_conn' /

  The name of the DBus connection.

* ``signal``

  / *Condition*: optional / *Type*: str / *Default*: '' /

  The name of the DBus signal to wait for.

* ``timeout``

  / *Condition*: optional / *Type*: int / *Default*: 0 /

  The maximum time (in seconds) to wait for the signal.

**Returns:**

* ``payloads``

  / *Type*: str /

  The signal payloads.
      """
      if conn_name not in self.connection_manage_dict.keys():
         raise Exception("The '%s' connection  hasn't been established. Please connect first." % conn_name)

      connection_obj = self.connection_manage_dict[conn_name]
      payloads = None
      try:
         payloads = connection_obj.wait_for_signal(signal, timeout)
      except AssertionError as ae:
         raise ae
      except Exception as ex:
         raise Exception(DBusManager.ERR_WAIT_DBUS_SIGNAL_STR % (signal, ex))

      return payloads

