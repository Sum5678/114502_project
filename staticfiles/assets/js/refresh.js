// refresh.js
function setupPullToRefresh(fetchFunction) {
  PullToRefresh.init({
    mainElement: 'body',
    onRefresh() {
      return fetchFunction();
    }
  });
}
