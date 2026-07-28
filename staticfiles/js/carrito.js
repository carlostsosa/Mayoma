let carrito = JSON.parse(localStorage.getItem("carrito") || "[]");

function actualizarWidget() {
    const widget = document.getElementById("cartWidget");
    const count = document.getElementById("cartCount");
    if (carrito.length === 0) {
        widget.style.display = "none";
    } else {
        widget.style.display = "inline-flex";
        count.textContent = carrito.reduce((s, i) => s + i.cantidad, 0);
    }
}

function agregarProducto(id, nombre, precio) {
    const existente = carrito.find(p => p.id === id);
    if (existente) {
        existente.cantidad += 1;
    } else {
        carrito.push({ id, nombre, precio, cantidad: 1 });
    }
    localStorage.setItem("carrito", JSON.stringify(carrito));
    actualizarWidget();
}

function eliminarProducto(id) {
    carrito = carrito.filter(p => p.id !== id);
    localStorage.setItem("carrito", JSON.stringify(carrito));
    actualizarWidget();
    renderCarrito();
}

function vaciarCarrito() {
    carrito = [];
    localStorage.setItem("carrito", JSON.stringify(carrito));
    actualizarWidget();
    renderCarrito();
}

function renderCarrito() {
    const tbody = document.getElementById("carritoItems");
    const totalEl = document.getElementById("carritoTotal");
    if (!tbody) return;
    if (carrito.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay productos en la cotización</td></tr>';
        totalEl.textContent = "$0.00";
        return;
    }
    let total = 0;
    tbody.innerHTML = carrito.map((p, i) => {
        const subtotal = p.cantidad * p.precio;
        total += subtotal;
        return `<tr>
            <td>${p.nombre}</td>
            <td><input type="number" class="form-control form-control-sm" style="width:80px" value="${p.cantidad}" min="1" onchange="cambiarCantidad(${i}, this.value)"></td>
            <td>$${parseFloat(p.precio).toFixed(2)}</td>
            <td>$${subtotal.toFixed(2)}</td>
            <td><button class="btn btn-danger btn-sm" onclick="eliminarProducto(${p.id})"><i class="bi bi-trash"></i></button></td>
        </tr>`;
    }).join("");
    totalEl.textContent = `$${total.toFixed(2)}`;
}

function cambiarCantidad(idx, val) {
    carrito[idx].cantidad = parseInt(val) || 1;
    localStorage.setItem("carrito", JSON.stringify(carrito));
    renderCarrito();
}

actualizarWidget();
