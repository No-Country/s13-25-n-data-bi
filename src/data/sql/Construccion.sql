SELECT * FROM "Compra";
SELECT * FROM "Lider";
SELECT  * FROM "MaterialConstruccion";
SELECT * FROM "Tipo";
SELECT * FROM "Proyecto";
SELECT    P."ID_Proyecto" , sum(c."Cantidad" *mc."Precio_Unidad" ) as  "Costo_Proyecto" from "DATA".CONSTRUCCION."Proyecto" p  natural join "DATA".CONSTRUCCION."MaterialConstruccion" mc natural join "DATA".CONSTRUCCION."Compra" c GROUP  by p."ID_Proyecto" ORDER  BY P."ID_Proyecto";
