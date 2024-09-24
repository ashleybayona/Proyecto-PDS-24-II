create database Proyecto1
use Proyecto1
create table Productos2 (
    ProductoID int primary key identity(1,1),
    Nombre nvarchar(100) NOT NULL,
    Precio decimal(10, 2) NOT NULL
);

create table Ordenes2 (
    OrdenID int primary key identity(1,1),
    FechaOrden  datetime default GETDATE(),
    Total decimal(10, 2) not null
);

create table OrdenesProductos2 (
    OrdenProductoID int primary key identity(1,1),
    OrdenID int foreign key references Ordenes2(OrdenID),
    ProductoID int foreign key references Productos2(ProductoID),
    Cantidad int not null
);
insert into  Productos2 (Nombre, Precio)
values 
('Producto A', 10.50),
('Producto B', 20.00),
('Producto C', 15.75);