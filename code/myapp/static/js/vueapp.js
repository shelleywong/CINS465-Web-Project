//adapted from: https://v1.vuejs.org/guide/events.html
var app1 = new Vue({
  el: '#app1',
  data: {
    msg: 'good to see you today!',
    name: 'World'
  },

  methods: {
    greet: function (event) {
      alert('Welcome ' + this.name + '! ' + this.msg)
    }
  }
})

//adapted from: https://vuejs.org/v2/guide/index.html
var app2 = new Vue({
  el: '#app2',
  data: {
    hovermessage: 'Thanks for visiting on ' + new Date().toLocaleString()
  }
})

var app_sugg = new Vue({
  el: '#app-suggestion',

  data: {
    suggestions: []
  },

  //Adapted from:
  //https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
  created: function() {
    this.fetchSuggestionList();
    this.timer = setInterval(this.fetchSuggestionList, 3000);
  },

  methods: {
    fetchSuggestionList: function() {
      $.get('/suggestions/',function(suggest_list) {
        this.suggestions = suggest_list.suggestions;
        //console.log(suggest_list);
      }.bind(this));
    },
    cancelAutoUpdate: function() { clearInterval(this.timer)}
  },

  beforeDestroy() {
    clearInterval(this.timer)
  }

})
