'use strict';
alert('sugma');
const containers = document.querySelectorAll('.container');

const draggable = function (event)

{
    // alert(event)
    console.log(event);
    // event.target.setAttribute(`style`, `order: 1; transition: all 1s ease-in;`)
}

containers.forEach(container => 
{
    container.addEventListener('mousedown', draggable);
})
