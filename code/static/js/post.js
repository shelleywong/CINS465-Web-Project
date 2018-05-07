var post_comment = new Vue({
  el: '#post-comment',

  data: {
    posts: []
  },

  //Adapted from:
  //https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
  created: function() {
    this.fetchPostList();
  },

  methods: {
    fetchPostList: function() {
      $.get('/message_board_posts/',function(post_list) {
        this.posts = post_list.posts;
      }.bind(this));
    },
  }
})
