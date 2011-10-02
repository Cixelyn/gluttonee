import api, re

def submit(restaurantID, tray, tip, dTime, first_name, last_name, addr, card_name, card_number, card_cvc, card_expiry, ccAddr):
  addr.validate()
  ccAddr.validate()
  if not re.match(api._checkNums, restaurantID):
    api._errs.append("o.submit - validation - restaurant ID (invalid, must be numerical)")
  if not re.match(api._checkCC, card_number):
    api._errs.append("o.submit - validation - credit card number (invalid)")
  if not re.match(api._checkNums, card_cvc):
    api._errs.append("o.submit - validation - credit card security code (invalid, must be numerical)")
  if (dTime.asap):
    date = "ASAP"
    time = ""
  else:
    date = dTime._strAPI("month") + "-" + dTime._strAPI("day")
    time = dTime._strAPI("hour") + ":" + dTime._strAPI("minute")
  return api._request("POST", "o", restaurantID, "tray=" + tray, "tip=" + tip, "delivery_date=" + date, "delivery_time=" + time, "first_name=" + first_name, "last_name=" + last_name, "addr=" + addr.street, "city=" + addr.city, "state=" + addr.state, "zip=" + addr.zip, "phone=" + addr.phone, "card_name=" + card_name, "card_number=" + card_number, "card_cvc=" + card_cvc, "card_expiry=" + card_expiry, "card_bill_addr=" + ccAddr.street, "card_bill_addr2=" + ccAddr.street2, "card_bill_city=" + ccAddr.city, "card_bill_state=" + ccAddr.state, "card_bill_zip=" + ccAddr.zip, "type=RES");
