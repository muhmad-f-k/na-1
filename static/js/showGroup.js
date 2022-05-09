var groupModal = document.getElementById("group-modal");
var memberModal = document.getElementById("member-modal");
var settingsModal = document.getElementById("settings-modal");
var profileModal = document.getElementById("profile-modal");
var commentForm = document.getElementById("comment-form");
var mainBg = document.querySelector(".profile-main");

function hideEditComment() {

  commentForm.classList.remove("show");
  commentForm.classList.add("hide");
}

function showEditComment() {

  commentForm.classList.add("show");
  commentForm.classList.remove("hide");
}

function hideGroupModal() {

    groupModal.classList.remove("show");
    groupModal.classList.add("hide");
    mainBg.classList.remove("blur")
  }

  function showGroupModal() {

    groupModal.classList.add("show");
    groupModal.classList.remove("hide");
    mainBg.classList.add("blur")
  }

  function showSettingsModal() {

    settingsModal.classList.add("show");
    settingsModal.classList.remove("hide");
    mainBg.classList.add("blur")
  }

  function hideSettingsModal() {

    settingsModal.classList.add("hide");
    settingsModal.classList.remove("show");
    mainBg.classList.remove("blur")
  }

  function showProfileModal() {

    profileModal.classList.add("show");
    profileModal.classList.remove("hide");
    mainBg.classList.add("blur")
  }

  function hideProfileModal() {

    profileModal.classList.add("hide");
    profileModal.classList.remove("show");
    mainBg.classList.remove("blur")
  }

  function showMemberModal() {
    memberModal.classList.add("show");
    memberModal.classList.remove("hide");
    mainBg.classList.add("blur")
  }

  function hideMemberModal() {
    memberModal.classList.remove("show");
    memberModal.classList.add("hide");
    mainBg.classList.remove("blur")
  }