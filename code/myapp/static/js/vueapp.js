var app1 = new Vue({
  el: '#app1',
  data: {
    msg: 'Hello Vue!'
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
        console.log(suggest_list);
      }.bind(this));
    },
    cancelAutoUpdate: function() { clearInterval(this.timer)}
  },

  beforeDestroy() {
    clearInterval(this.timer)
  }

})
