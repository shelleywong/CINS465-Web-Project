
var app_roster = new Vue({
  el: '#app-roster',

  data: {
    users: [],
    load: true,
    first: false,
    last: false,
    username: false,
    selected: 'A',
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
        // this.orderedUsers =_.orderBy(this.users, 'last_name')
        // this.users = this.users.orderBy(this.users,'last_name')
        console.log(this.selected);
      }.bind(this));
    },
  },


  // computed: {
  //   orderedUsers: function () {
  //     return _.orderBy(this.users, 'last_name')
  //   }
    // orderedUsers() {
    //   var self = this;
    //   return self.orderBy(this.users,'last_name');
    // }
  // },
})
