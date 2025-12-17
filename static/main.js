const form = document.getElementById("giftForm")
const giftsContainer = document.getElementById("gifts");

async function loadGifts() {
    const response = await fetch('/gifts');
    const gifts = await response.json();
    
    giftsContainer.innerHTML = '';
    gifts.forEach(gift => {
        const item = document.createElement("div");
        item.className = "w3-card w3-margin-bottom w3-padding";
        
        const label = document.createElement("label");
        label.className = "gift-item";
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "w3-check";
        checkbox.checked = gift.completed;
        checkbox.addEventListener("change", async () => {
            await fetch(`/gifts/${gift.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ completed: checkbox.checked })
            });
            text.style.textDecoration = checkbox.checked ? "line-through" : "none";
            text.style.color = checkbox.checked ? "#999" : "#000";
        });
        
        const text = document.createElement("span");
        text.textContent = `Gift for ${gift.name}: ${gift.gift}`;
        if (gift.completed) {
            text.style.textDecoration = "line-through";
            text.style.color = "#999";
        }
        
        label.appendChild(checkbox);
        label.appendChild(text);
        item.appendChild(label);
        giftsContainer.appendChild(item);
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = form.elements.name.value;
    const gift = form.elements.gift.value;

    await fetch('/gifts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, gift })
    });

    form.reset();
    await loadGifts(); 
});

loadGifts();