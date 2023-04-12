bool isInteger(String? s) {
 if (s == null) {
   return false;
 }
 return int.tryParse(s) != null;
}

int? getInteger(String? s){
  if(isInteger(s) == false) return null;
  
  return int.tryParse(s!);
}

bool isDouble(String? s) {
 if (s == null) {
   return false;
 }
 return double.tryParse(s) != null;
}

double? getDouble(String? s){
  if(isDouble(s) == false) return null;
  
  return double.tryParse(s!);
}