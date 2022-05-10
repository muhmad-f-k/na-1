var btnAdd = document.getElementById('add');
var btnRemove = document.getElementById('remove');
var input = document.getElementById('input');

btnAdd.addEventListener('click', () => {
    input.value = parseInt(input.value) + 1;
});

btnRemove.addEventListener('click', () => {
    if (input.value == 1) {
        input.value = input.value;
    }
    else {
        input.value = parseInt(input.value) - 1;
    }

});