import 'package:flutter/foundation.dart';

/// class is used to store user details
class UserModel extends ChangeNotifier{
  late String _serverAddress;
  late String _clientId;
  bool _isAuthenticated = false; 

  String get serverAddress{
    return _serverAddress;
  }

  set serverAddress(String serverAddress){
    _serverAddress = serverAddress;
  }

  String get clientId{
    return _clientId;
  }

  set clientId(String clientId){
    _clientId = clientId;
  }

  bool get isAuthenticated{
    return _isAuthenticated;
  }

  set isAuthenticated(bool isAuthenticated){
    _isAuthenticated = isAuthenticated;
    notifyListeners();
  }
}