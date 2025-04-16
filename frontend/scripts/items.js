const baseURL = "http://localhost:8000";

async function loadItems(searchTerm = "") {
  const res = await fetch(`${baseURL}/items`);
  const data = await res.json();
  const list = document.getElementById("itemList");
  list.innerHTML = "";

  const filteredItems = data.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  document.getElementById("itemCount").textContent = `Total items: ${filteredItems.length}`;

  filteredItems.forEach(item => {
    const li = document.createElement("li");
    li.className = "item-card";
    
    li.innerHTML = `
      <div class="item-content">
        <h3>${item.name}</h3>
        <p>${item.description}</p>
      </div>
    `;
    
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-btn";
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => deleteItem(item._id);
    
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

async function deleteItem(id) {
  await fetch(`${baseURL}/items/${id}`, { method: "DELETE" });
  loadItems(document.getElementById("search").value); 
}

document.getElementById("search").addEventListener("input", (e) => {
  loadItems(e.target.value); 
});

document.getElementById("itemForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const description = document.getElementById("description").value;
  await fetch(`${baseURL}/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description })
  });
  e.target.reset();
  loadItems(document.getElementById("search").value);
});

// Initialize the list
loadItems();