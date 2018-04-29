var next_image = new Vue({
  el: '#next-image',

  data: {
    counter: 0,
  }
})

var app_student = new Vue({
  el: '#app-student',

  data: {
    users: [],
    curscore: [],
    i: 0,
    cur_student: {},
  },

  //Adapted from:
  //https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
  created: function() {
    this.fetchStudentList();
  },

  methods: {
    fetchStudentList: function() {
      $.get('/people/students/',function(user_list) {
        this.users = user_list.users;
        this.playgame();
        //console.log(user_list);
      }.bind(this));
    },
    playgame: function(){
      console.log(this.users[this.i].username);
      this.cur_student = this.users[this.i].username;
      console.log(this.cur_student);
    },

    // setCurStudent: function(data){
    //   this.$set(this.cur_student, data);
    // },

  },
})
