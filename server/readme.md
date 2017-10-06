TODO:
Back-end
0. Refactor Database Schema
1. Database mirgration
2. Control logs of all users
3. Refactor Database connection
4. check logic and flow of update function of product's orignal price
5. API valid token utils.
6. Renaming api end-point => get<FunctionName>Url
Font-end:
1. Loading
2. Empty result
3. Show error
4. Format moneny


Temporary Document

1. Change database:
 - Order Item:
  + alter table order_item drop column purchase_price;
  + alter table order_item add original_price DECIMAL(10,2) DEFAULT 0;
  + alter table order_item add actual_paid_price DECIMAL(10,2) DEFAULT 0;