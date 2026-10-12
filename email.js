// Writes the support address at runtime so it is not sitting in the page source for scrapers.
document.querySelectorAll('.email').forEach(function (el) {
  var u = 'laddothis', d = 'gmail.com';
  el.innerHTML = '<a href="ma' + 'ilto:' + u + '@' + d + '?subject=Construction%20Takeoff%20-%20Tally">' + u + '@' + d + '</a>';
});
