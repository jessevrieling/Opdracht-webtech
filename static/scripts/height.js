window.onload = function() {
    var houseCards = document.querySelectorAll('.house-card');
    var maxHeight = 0;
    
    houseCards.forEach(function(card) {
        maxHeight = Math.max(maxHeight, card.offsetHeight);
    });
    
    houseCards.forEach(function(card) {
        card.style.height = maxHeight -100 + 'px';
    });
};
