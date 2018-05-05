var app_student = new Vue({
  el: '#app-student',

  data: {
    users: [],
    curscore: [],
    i: 0,
    cur_student: {},
    // users_except_cur: [],
    multiple_choice: [],
    checked_name: "",
    checked_names: [],
    score: 0,
    percent_score: 0,
    fin: false,
  },

  //Adapted from:
  //https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
  created: function() {
    this.fetchStudentList();
  },

  methods: {
    fetchStudentList: function() {
      $.get('/people/students/',function(user_dictionary) {
        this.users = user_dictionary.users;
        this.multiple_choice = this.users.slice();
        this.checked_names = this.users.slice();
        this.playgame();
        // console.log(this.multiple_choice);
      }.bind(this));
    },
    playgame: function(){
      console.log(this.users[this.i].username);
      //initialize variables
      var rand = [];
      this.cur_student = this.users[this.i].username;
      this.score = 0;
      this.multiple_choice = [];
      this.checked_names = [];
      this.fin = false;
      //ensure current student is one of the multiple choice options, then add
      //three other unique random students to the multiple choice options
      this.multiple_choice.push(this.users[this.i]);
      rand.push(this.i);
      this.randIndex(rand);
      console.log(rand);
      console.log(this.multiple_choice);
    },

    nextImage: function() {
      var rand = [];
      //add user's selection to checked_names list; if correct, increase score
      this.checked_names.push(this.checked_name);
      if(this.checked_name == this.users[this.i].first_name){
        this.score += 1;
        this.curscore.push(1);
      }
      else {
        this.curscore.push(0);
      }
      //if there are still more students in the list, set new current student
      //and new random set of multiple choice options
      if(this.i < this.users.length-1) {
        this.i += 1;
        this.checked_name = "";
        this.cur_student = this.users[this.i].username;
        this.shuffle(this.multiple_choice);
        this.multiple_choice = [];
        rand.push(this.i);
        this.multiple_choice.push(this.users[this.i]);
        this.randIndex(rand);
        console.log(rand);
        this.shuffle(this.multiple_choice);
      }
      else {
        this.showResults();
        console.log("finished with array");
      }
    },

    //adapted from:
    //https://stackoverflow.com/questions/2380019/generate-unique-random-numbers-between-1-and-100?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    randIndex: function(array) {
      while(array.length < 4){
        var randomnumber = Math.floor(Math.random()*this.users.length);
        if(array.indexOf(randomnumber) > -1) continue;
        array[array.length] = randomnumber;
        this.multiple_choice.push(this.users[randomnumber]);
      }
    },

    //adapted from Fisher-Yates (aka Knuth) Shuffle:
    //https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
    shuffle: function(array) {
      var currentIndex = array.length, tempValue, randomIndex;

      // While there remain elements to shuffle...
      while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        tempValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = tempValue;
      }
    },

    showResults: function() {
      this.fin = true;
      this.percent_score = (this.score/this.users.length)*100;
    },

  },
})


// var copy_student = new Vue({
//   el: '#copy-student',
//
//   data: {
//     users_copy: [],
//     curscore: [],
//     i: 0,
//     cur_student: {},
//   },
//
//   //Adapted from:
//   //https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
//   created: function() {
//     this.fetchStudentCopy();
//   },
//
//   methods: {
//     fetchStudentCopy: function() {
//       $.get('/people/students/',function(user_list) {
//         this.users_copy = user_list.users_copy;
//         this.playgame();
//         //console.log(user_list);
//       }.bind(this));
//     },
//     playgame: function(){
//       console.log(this.users_copy[this.i].username);
//
//       this.cur_student = this.users_copy[this.i].username;
//       // console.log(this.cur_student);
//
//     },
//     nextImage: function() {
//       this.i += 1;
//       this.cur_student = this.users_copy[this.i].username;
//     },
//     // ready: function() {
//     //     this.users_except_cur = this.users;
//     // }
//
//   },
// })
