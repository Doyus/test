document.addEventListener('DOMContentLoaded', function() {
  var startUrlsInput = document.getElementById('start-urls');
  var projectNameInput = document.getElementById('project-name');
  if (!startUrlsInput || !projectNameInput) {
        console.error('Error: Could not find input elements');
        return;
      }
  function updateProjectName() {
    var startUrl = startUrlsInput.value;
    if (startUrl) {
      var domain = startUrl.replace(/^(https?:\/\/)?(www\.)?/, '').split('/')[0];
      var projectName = domain.replace(/\./g, '_');
      projectNameInput.value = projectName;
    } else {
      projectNameInput.value = '';
    }
  }

  function handleKeyDown(event) {
    if (event.keyCode === 13) { // 13 is the key code for Enter
      updateProjectName();
    }
  }

  startUrlsInput.addEventListener('blur', updateProjectName);
  startUrlsInput.addEventListener('keydown', handleKeyDown);
});