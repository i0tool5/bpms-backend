const store = new Vuex.Store({
    state: {
        csrftoken: getCookie('csrftoken'),
        statuses: [
            {
                id: 1,
                "display_name": "Открыта"
            },
            {
                id: 2,
                "display_name": "В работе"
            },
            {
                id: 3,
                "display_name": "Закрыта"
            }
        ],

        priorities: [
            {
                "value": 1,
                "display_name": "Низкий"
            },
            {
                "value": 2,
                "display_name": "Ниже среднего"
            },
            {
                "value": 3,
                "display_name": "Средний"
            },
            {
                "value": 4,
                "display_name": "Выше среднего"
            },
            {
                "value": 5,
                "display_name": "Высокий"
            },
            {
                "value": 6,
                "display_name": "Реального времени"
            }
        ],
    },
}) 

// End of Vuex store

async function post(url="", csrftoken, data){
    const response = await fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFTOKEN': csrftoken,
            'Content-Type': 'application/json',
        },
        body: data,
    })
    return response
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// End of helper functions


const ProjCreate = ("project-create-form", {
    props: [
        "elements",
    ],
    data: function(){
        return {
            task_form_visible: false,
            proj: {
                name: "",
                payment: 10000,
                begin_date: "",
                end_date: "",
                description: "",
                tasksforprojects: [],
            },
            task: {
                task_name: "prepared task",
                assign: ["2"],
                begin_date: "2020-12-01",
                end_date: "2020-12-21",
                status: "1",
                priority: "3",
                description: "None",
            },
            tasks: []
        }
    },
    methods: {
        sendFormData: function(){
            // this.proj.tasksforprojects.push(this.task)
            dat = this.proj
            sndData = JSON.stringify(dat)

            post("/api/projects.json", this.$store.state.csrftoken, sndData)
                .then(
                    response => {
                        if (response.ok) {
                            return response.json()
                        } else {
                            return response.json()
                        }
                    })
                .then(
                    json => {     
                        if(json !== undefined) {
                            this.elements.unshift(json)
                            this.$emit("closemodal")
                        }
                    })
        },
    },
    template: `
    <form id="proj-task-form" v-on:submit.prevent=sendFormData>
        <div>
            <div>
                <label>Название проекта:</label>
                <input v-model="proj.name" type="text" name="name" maxlength="128" placeholder="Название" required class="w-100">
            </div>
            <div style="margin-top: 10px;">
                <label>Сумма</label>
                <input v-model="proj.payment" type="number" name="payment" value="100000" required class="w-100">
            </div>
            <div style="margin-top: 10px;">
                <label>Дата начала:</label>
                <input v-model="proj.begin_date" type="date" name="begin_date" required>
            </div>
            <div style="margin-top: 10px;">
                <label>Дата окончания:</label>
                <input v-model="proj.end_date" type="date" name="end_date" required>
            </div>
            <div style="margin-top: 10px;">
                <label>Описание:</label>
                <textarea v-model="proj.description" name="description" cols="40" rows="10" maxlength="1000" id="id_description" class="w-100"></textarea>
            </div>
            <div>
                <a class="button btn-blue w-100" @click="task_form_visible = !task_form_visible">Развернуть форму</a>
            </div>
            <div v-bind:class="[{'visible': task_form_visible}, 'invisible']" id="task-form-container">
                <div class="task-container">
                    <div>
                        <label>Название задачи</label>
                        <input v-model="task.task_name" name="task_name" type="text" maxlength="80">
                    </div>
                    <div>
                        <label>Дата начала</label>
                        <input v-model="task.begin_date" name="task_begin_date" type="date">
                    </div>
                    <div>
                        <label>Дата окончания</label>
                        <input v-model="task.end_date" name="task_end_date" type="date">
                    </div>
                    <div>
                        <label>Статус</label>
                        <input v-model="task.status" name="task_status" type="number">
                    </div>
                    <div>
                        <label>Приоритет</label>
                        <input name="task_prio" value="3" type="number">
                    </div>
                    <div>
                        <label>Назначена</label>
                        <input v-model="task.assign" name="task_assign" type="number" value="2">
                    </div>
                    <div>
                        <label>Описание</label>
                        <textarea v-model="task.description" name="task_description"></textarea>
                    </div>
                </div>
            </div>
        </div>
    </form>
    `,
})

const ProjChange = ("project-change-form", {
    props: ["proj_obj"],
    data(){
        return {
            n: "",
            p: this.proj_obj.payment,
            b_d: "",
            e_d: "",
            descr: "",
        }
    },
    methods: {
        update: function() {
            let r = {
                name: this.n,
                payment: this.p,
                begin_date: this.b_d,
                end_date: this.e_d,
                description: this.descr
            }
            console.log(JSON.stringify(r))
        }
    },
    
    template: `
    <div>
        <div>
            <input v-model="n" type="text" :placeholder="proj_obj.name">
        </div>
        <div>
            <input v-model="p" type="number" :placeholder="proj_obj.payment">
        </div>
        <div>
            <input v-model="b_d" type="date">
        </div>
        <div>
            <input v-model="e_d" type="date">
        </div>
        <div>
            <textarea v-model="descr" :placeholder="proj_obj.description"></textarea>
        </div>
        <button class="button btn-green" @click=update>Обновить</button>
    </div>
    `
})

var projectsApp = new Vue({
    el: "#app-projects",
    delimiters: ["[[", "]]"],
    store: store,

    components: {
        'project-create-form': ProjCreate,
        'project-change-form': ProjChange, 
    },

    data: {
        elements: [],
        del_elements: [],
        ch_elem: Object(),
        modal_visible: false,
    },

    computed: {
        numMarked: function() {
            return this.del_elements.length
        }
    },

    mounted() {
        fetch("/api/projects.json")
            .then(response => response.json())
            .catch(err => console.log(err))
            .then(json => this.elements = json.results)
    },

    methods: {
        updateElement: function(event){
            const uid = event.target.parentElement.querySelector("[class='identificator']").value
            let x = this.elements.find(el => el.a_uid === uid)
            this.ch_elem = x
        },
        deleteElement: function(event){
            const uid = event.target.parentElement.querySelector("[class='identificator']").value
            let uri = `api/projects/${uid}/`
            fetch(uri, {
                method: "DELETE",
                headers: {
                    Accept: "application/json",
                    "X-CSRFTOKEN": this.$store.state.csrftoken,
                },
            }).then(response => {
                if(response.ok)
                {
                    this.elements = this.elements.filter(el => el.a_uid != uid)
                }
            }).catch(err => console.log("Error ocured:" + err))
        },
        deleteMarked: function() {
            const data = JSON.stringify({"projects": this.del_elements})
            fetch("api/projects/delete-multiple/", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFTOKEN": this.token,
                    Accept: "application/json",
                },
                body: data,
            }).then(response => {
                if (response.status === 204) {
                    this.elements = this.elements.filter(el => !this.del_elements.includes(el.a_uid))
                    this.del_elements = []
                } else {
                    window.console.log("Error")
                }
            })
        }
    }
})

// End of projects application

const DealCreate = ("deal-create-form", {
    props: [
        "elements",
    ],
    data() {
        return {
            deal: {
                name: "",
                payment: 10000,
                description: "",
                client: "",
                status: null,
                assigned: null,
            }
        } 
    },
    methods: {
        sendFormData: function(){
            dat = this.deal
            sndData = JSON.stringify(dat)

            post("/api/deals.json", getCookie('csrftoken'), sndData)
                .then(
                    response => {
                        if (response.ok) {
                            return response.json()
                        } else {
                            return response.json()
                        }
                    })
                .then(
                    json => {     
                        if(json !== undefined) {
                            this.elements.unshift(json)
                            this.$emit("closemodal")
                        }
                    })
        },
    },

    template: `
    <form id="deal-form" v-on:submit.prevent=sendFormData>
        <div>
            <div>
                <label>Название :</label>
                <input v-model="deal.name" type="text" name="name" maxlength="128" placeholder="Например Сделка №1" required class="w-100">
            </div>
            <div style="margin-top: 10px;">
                <label>Сумма:</label>
                <input v-model="deal.payment" type="number" name="payment" required class="w-100">
            </div>
            <div style="margin-top: 10px;">
                <label>Название компании:</label>
                <input v-model="deal.client" class="w-100" type="text" maxlength="128" placeholder="ICreate Company">
            </div>
            <div style="margin-top: 10px;">
                <label>Статус:</label>
                <p>Select status</p>
            </div>
            <div style="margin-top: 10px;">
                <label>Описание:</label>
                <textarea v-model="deal.description" name="description" cols="40" rows="10" maxlength="1000" id="id_description" class="w-100"></textarea>
            </div>
        </div>
    </form>
    `
})


var dealsApp = new Vue({
    el: "#app-deals",
    delimiters: ["[[", "]]"],
    store: store,
    data() {
        return {
            elements: [],
            del_elements: [],
            modal_visible: false,
        }
    },
    components: {
        "deal-create": DealCreate,
    },

    methods: {
        deleteElement: function(event){
            const uid = event.target.parentElement.querySelector("[class='identificator']").value
            let uri = `api/deals/${uid}/`
            fetch(uri, {
                method: "DELETE",
                headers: {
                    Accept: "application/json",
                    "X-CSRFTOKEN": this.$store.state.csrftoken,
                },
            }).then(response => {
                if(response.ok)
                {
                    this.elements = this.elements.filter(el => el.a_uid != uid)
                }
            }).catch(err => console.log("Error ocured:" + err))
        },
    },

    mounted() {
        fetch("/api/deals.json")
            .then(response => {
                if(response.status === 200){
                    return response.json()
                }
            }).then(json => {this.elements = json.results})
    }
})

// End of deal application

const TaskCreate = ("task-create-form", {
    props: ["elements"],
    data() {
        return {
            task: {
                task_name: "",
                assign: [],
                begin_date: "",
                end_date: "",
                status: 1,
                priority: 1,
                description: "",
            },

            statuses: this.$store.state.statuses,
            priorities: this.$store.state.priorities,
        }
    },
    methods: {
        sendFormData: function() {
            console.log(this.task)
        }
    },

    template: `
    <form id="task-form" v-on:submit.prevent=sendFormData>
        <div>
            <div>
                <label>Название</label>
                <input v-model="task.task_name" class="w-100" type="text">
            </div>
            <div style="margin-top: 10px;">
                <label>Дата начала</label>
                <input v-model="task.begin_date" type="date">
            </div>
            <div style="margin-top: 10px;">
                <label>Дата окончания</label>
                <input v-model="task.end_date" type="date">
            </div>
            <div style="margin-top: 10px;">
                <label>Статус</label>
                <select name="status" v-model="task.status">
                    <option
                        v-for="status in statuses"
                        :value=status.id
                    >{{ status.display_name }}</option>
                </select>
            </div>
            <div style="margin-top: 10px;">
                <label>Приоритет</label>
                <select v-model="task.priority">
                    <option
                        v-for="priority in priorities"
                        :value=priority.value
                    >{{ priority.display_name }}</option>
                </select>
            </div>
            <div style="margin-top: 10px;">
                <label>Описание</label>
                <textarea class="w-100" v-model="task.description"></textarea>
            </div>
        </div>
    </form>
    `,
})

var tasksApp = new Vue({
    el: "#app-tasks",
    store: store,
    delimiters: ["[[", "]]"],

    components: {
        "task-create": TaskCreate,
    },

    data() {
        return {
            elements: [],
            modal_visible: false,
            users: [
                {id: 1, name: "alex"},
            ]
        }
    },

    mounted() {
        fetch("api/tasks.json")
            .then(response => {
                if(response.status == 200){
                    return response.json();
                }
            }).then(json => {this.elements = json.results})
    },

    methods: {
        getUsers: function (el) {
            let user = this.users.find(user => {return user.id == el});
            return user.name;
        },

        getStatus: function (id) {
            var statuses = this.$store.state.statuses;
            var s = statuses.find(status => status.id == id);
            return s.display_name;
        },

        getPrio: function(val) {
            var prios = this.$store.state.priorities;
            var p = prios.find(prio => prio.value == val)
            return p.display_name;
        },

        deleteElement: function(ev) {
            const uid = ev.target.parentElement.querySelector(".identificator").value;
            let uri = `api/tasks/${uid}/`;
            fetch(uri, {
                method: "DELETE",
                headers: {
                    Accept: "application/json",
                    "X-CSRFTOKEN": this.$store.state.csrftoken,
                },
            }).then(response => {
                if(response.ok)
                {
                    this.elements = this.elements.filter(el => el.id != uid)
                }
            }).catch(err => console.log("Error ocured:" + err))
        },
    }
})
