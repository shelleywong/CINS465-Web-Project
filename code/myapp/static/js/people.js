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
        // this.multiple_choice = this.users.slice(0,1);
        this.multiple_choice = this.users.slice();
        this.checked_names = this.users.slice();
        this.playgame();
        // console.log(this.multiple_choice);
      }.bind(this));
    },
    playgame: function(){
      console.log(this.users[this.i].username);
      this.cur_student = this.users[this.i].username;
      var rand = [];
      this.multiple_choice = [];
      this.checked_names = [];
      rand.push(this.i);
      // this.multiple_choice = this.users.slice(0,1);
      // this.multiple_choice[0] = this.users[this.i];
      this.multiple_choice.push(this.users[this.i]);
      while(rand.length < 4){
          var randomnumber = Math.floor(Math.random()*this.users.length);
          if(rand.indexOf(randomnumber) > -1) continue;
          rand[rand.length] = randomnumber;
          this.multiple_choice.push(this.users[randomnumber]);
      }      // console.log(this.cur_student);
      console.log(rand);
      console.log(this.multiple_choice);
    },

    nextImage: function() {

      if(this.i < this.users.length-1) {
        this.i += 1;
        this.cur_student = this.users[this.i].username;
        this.shuffle(this.multiple_choice);
        this.checked_names.push(this.checked_name);
        //adapted from: https://stackoverflow.com/questions/2380019/generate-unique-random-numbers-between-1-and-100?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        var rand = [];
        this.multiple_choice = [];
        rand.push(this.i);
        this.multiple_choice.push(this.users[this.i]);
        while(rand.length < 4){
            var randomnumber = Math.floor(Math.random()*this.users.length);
            if(rand.indexOf(randomnumber) > -1) continue;
            rand[rand.length] = randomnumber;
            this.multiple_choice.push(this.users[randomnumber]);
        }
        console.log(rand);
        this.shuffle(this.multiple_choice);
      }
      else {
        console.log("finished with array");
      }
      // this.i += 1;
      // this.cur_student = this.users[this.i].username;
      // this.shuffle(this.multiple_choice);
      // //adapted from: https://stackoverflow.com/questions/2380019/generate-unique-random-numbers-between-1-and-100?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
      // var rand = [];
      // this.multiple_choice = [];
      // rand.push(this.i);
      // this.multiple_choice.push(this.users[this.i]);
      // while(rand.length < 4){
      //     var randomnumber = Math.floor(Math.random()*this.users.length);
      //     if(rand.indexOf(randomnumber) > -1) continue;
      //     rand[rand.length] = randomnumber;
      //     this.multiple_choice.push(this.users[randomnumber]);
      // }
      // console.log(rand);
      // this.shuffle(this.multiple_choice);
    },

    // randIndex: function(index) {
    //   var rand = [];
    //   rand.push(index);
    //   this.multiple_choice.push(this.users[index]);
    //   while(rand.length < 4){
    //       var randomnumber = Math.floor(Math.random()*this.users.length) + 1;
    //       if(this.rand.indexOf(randomnumber) > -1) continue;
    //       rand[rand.length] = randomnumber;
    //       this.multiple_choice.push(this.users[randomnumber]);
    //   }
    //   console.log(this.multiple_choice);
    // },

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

    // saveGuess: function() {
    //   checked_names.push_back(this.checked_name);
    // },

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
