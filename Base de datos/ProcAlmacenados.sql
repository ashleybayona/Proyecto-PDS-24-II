--PROCEDIMIENTOS ALMACENADOS -> está en la base de datos pero aki tmb por si acaso

--CREAR VENTA
create proc CrearVenta
@IdUsuario int
as 
begin
	declare @CodigoBoleta nvarchar(10)
	declare @IdVenta int

	--para generar 8 char aleatorios para el codigoboleta
	while 1=1
    begin
        set @CodigoBoleta = left(newid(), 8);  
        if not exists (select 1 from Venta where CodigoBoleta = @CodigoBoleta)
        break;
    end

	insert into Venta (IdUsuario, ImporteVenta, ImporteIGV, ImporteTotal, Fecha, CodigoBoleta, Estado)
	values (@IdUsuario, 0, 0, 0, GETDATE(), @CodigoBoleta, 0)

	set @IdVenta = SCOPE_IDENTITY() --obtiene el id recién creado
	select @IdVenta as IdVenta --retorna el id creado al front
end

--AGREGAR PRODUCTOS AL DETALLEVENTA
create proc AgregarProductosDetalleVenta
@IdVenta int, 
@IdProducto int,
@Cantidad int
as
begin
	declare @PrecioUnitario decimal(7,2)
	declare @Precio decimal (7,2)

	--para obtener el precio unitario del producto segun su id
	select @PrecioUnitario = PrecioUnitario from Producto where IdProducto = @IdProducto

	--calcular el precio debido a la cant y preciounit
	set @Precio = @Cantidad * @PrecioUnitario

	insert into DetalleVenta (IdVenta, IdProducto, Cantidad, PrecioUnitario, Precio)
	values (@IdVenta, @IdProducto, @Cantidad, @PrecioUnitario, @Precio)
end

--ACTUALIZAR LOS IMPORTES DE LA TABLA VENTA -> esto pq fueron inicializados en 0 para llenar DetalleVenta
create proc ActualizarImportesVenta
@IdVenta int
as 
begin
	declare @ImporteVenta decimal (7,2)
	declare @ImporteIGV decimal(7,2)
	declare @ImporteTotal decimal (7,2)

	--hallar el importe venta como la sum de precios donde el idventa sea el mismo en detalleventa
	select @ImporteVenta = SUM(Precio) from DetalleVenta where IdVenta = @IdVenta

	--calcular los otros importes
	set @ImporteIGV = @ImporteVenta * 0.18
	set @ImporteTotal = @ImporteVenta + @ImporteIGV

	--actualizamos con update table
	update Venta
	set
		ImporteVenta = @ImporteVenta,
		ImporteIGV = @ImporteIGV,
		ImporteTotal = @ImporteTotal
	where IdVenta = @IdVenta
end