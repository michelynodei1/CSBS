const menu = document.querySelector(".menu"); // get menu item for click event

menu.addEventListener("click", function () {
    expandSidebar();
    showHover();

});

/**
 * expand sidebar if it is short, otherwise collapse it
 */
function expandSidebar() {
    document.querySelector("body").classList.toggle("short");
    let keepSidebar = document.querySelectorAll("body.short");
    if (keepSidebar.length === 1) {
        localStorage.setItem("keepSidebar", "true");
    } else {
        localStorage.removeItem("keepSidebar");
    }
}

/**
 * show hover effect on sidebar
 */
function showHover() {
    const li = document.querySelectorAll(".short .sidebar li a");
    if (li.length > 0) {
        li.forEach(function (item) {
            item.addEventListener("mouseover", function () {
                const text = item.querySelector(".text");
                text.classList.add("hover");
            });
            item.addEventListener("mouseout", function () {
                const text = item.querySelector(".text");
                text.classList.remove("hover");
            });
        });
    }
}


/**
 * get search button click if short sidebar or mobile
 */
function getSearch() {
    document.querySelector(".callSearch").addEventListener("click", function (e) {
        e.preventDefault();
        if (
            document.querySelector("body").classList.contains("short") ||
            window.innerWidth <= 844
        ) {
            document.querySelector(".searchWindow").classList.toggle("active");
        }
    });
    document
        .querySelector(".cancelSearch")
        .addEventListener("click", function () {
            document.querySelector(".searchWindow").classList.toggle("active");
        });
}

/**
 * check local storage for keep sidebar
 */
function showStoredSidebar() {
    if (localStorage.getItem("keepSidebar") === "true") {
        document.querySelector("body").classList.add("short");
        showHover();
        getSearch();
    }
}

showStoredSidebar(); // show sidebar if stored in local storage
/**Tab Contents  */
function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

//To Do List Js
window.addEventListener('load', () => {
    todos = JSON.parse(localStorage.getItem('todos')) || [];
    const nameInput = document.querySelector('#name');
    const newTodoForm = document.querySelector('#new-todo-form');

    const username = localStorage.getItem('username') || '';

    nameInput.value = username;

    nameInput.addEventListener('change', (e) => {
        localStorage.setItem('username', e.target.value);
    })

    newTodoForm.addEventListener('submit', e => {
        e.preventDefault();

        const todo = {
            content: e.target.elements.content.value,
            category: e.target.elements.category.value,
            done: false,
            createdAt: new Date().getTime()
        }

        todos.push(todo);

        localStorage.setItem('todos', JSON.stringify(todos));

        // Reset the form
        e.target.reset();

        DisplayTodos()
    })

    DisplayTodos()
})

function DisplayTodos() {
    const todoList = document.querySelector('#todo-list');
    todoList.innerHTML = "";

    todos.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item');

        const label = document.createElement('label');
        const input = document.createElement('input');
        const span = document.createElement('span');
        const content = document.createElement('div');
        const actions = document.createElement('div');
        const edit = document.createElement('button');
        const deleteButton = document.createElement('button');

        input.type = 'checkbox';
        input.checked = todo.done;
        span.classList.add('bubble');
        if (todo.category == 'personal') {
            span.classList.add('personal');
        } else {
            span.classList.add('business');
        }
        content.classList.add('todo-content');
        actions.classList.add('actions');
        edit.classList.add('edit');
        deleteButton.classList.add('delete');

        content.innerHTML = `<input type="text" value="${todo.content}" readonly>`;
        edit.innerHTML = 'Edit';
        deleteButton.innerHTML = 'Delete';

        label.appendChild(input);
        label.appendChild(span);
        actions.appendChild(edit);
        actions.appendChild(deleteButton);
        todoItem.appendChild(label);
        todoItem.appendChild(content);
        todoItem.appendChild(actions);

        todoList.appendChild(todoItem);

        if (todo.done) {
            todoItem.classList.add('done');
        }

        input.addEventListener('change', (e) => {
            todo.done = e.target.checked;
            localStorage.setItem('todos', JSON.stringify(todos));

            if (todo.done) {
                todoItem.classList.add('done');
            } else {
                todoItem.classList.remove('done');
            }

            DisplayTodos()

        })

        edit.addEventListener('click', (e) => {
            const input = content.querySelector('input');
            input.removeAttribute('readonly');
            input.focus();
            input.addEventListener('blur', (e) => {
                input.setAttribute('readonly', true);
                todo.content = e.target.value;
                localStorage.setItem('todos', JSON.stringify(todos));
                DisplayTodos()

            })
        })

        deleteButton.addEventListener('click', (e) => {
            todos = todos.filter(t => t != todo);
            localStorage.setItem('todos', JSON.stringify(todos));
            DisplayTodos()
        })

    })
<<<<<<< Updated upstream
}
=======
}

// Overview Javascript on tabs 
function vopenCity(evt, cityName) {
	var i, x, tablinks;
	x = document.getElementsByClassName("city");
	for (i = 0; i < x.length; i++) {
	   x[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablink");
	for (i = 0; i < x.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" w3-red", ""); 
	}
	document.getElementById(cityName).style.display = "block";
	evt.currentTarget.className += " w3-red";
  }
  $(document).ready(function(){
    var socket = io.connect("http://localhost:5000");
    socket.on( 'connect', function() {
        socket.send("User connected!" );
    });
    socket.on( 'message', function(data){
        $('#messages').append($('<p>').text(data));
    });
    $('#sendBtn').on('click',function() {
        socket.send($('#username').val()+':'+$('#message').val());
        $('#message').val('');
    });
})
  



  /* jQuery call to the accordion() method.*/
$(document).ready(function() {
    $("#accordion").accordion(
            {
            
            })
});

 
>>>>>>> Stashed changes
