document.addEventListener("DOMContentLoaded", function () {
    // Tabs 
  const personalInformationTab = document.getElementById("personal-information-tab");
  const personalSecurityTab = document.getElementById("personal-security-tab");
  // const cardInformationTab = document.getElementById("card-information-tab");
  const balanceTab = document.getElementById("balance-tab");
  const activityTab = document.getElementById("activity-tab");

    // Section 
  const personalInformationSection = document.getElementById("personal-information-section");
  const personalSecuritySection = document.getElementById("personal-security-section");
  // const cardInformationSection = document.getElementById("card-information-section");
  const balanceSection = document.getElementById("balance-section");
  const activitySection = document.getElementById("activity-section");
  const accountOverviewSection = document.getElementById("account-overview-section");
  const accountPageSection = document.getElementById("account-page-section");

  
  // Function to remove "active" class from all tabs
  function resetTabs() {
    personalInformationTab.classList.remove("active");
    personalSecurityTab.classList.remove("active");
    // cardInformationTab.classList.remove("active");
    balanceTab.classList.remove("active");
    activityTab.classList.remove("active");
  }

  // Show orders-section by default and hide positions-section
  personalInformationSection.style.display = "block";
  personalSecuritySection.style.display = "none";
  // cardInformationSection.style.display = "none";
  balanceSection.style.display = "none";
  activitySection.style.display = "none";
  accountOverviewSection.style.display="block";



  // Add event listener to orders-tab
  personalInformationTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Show orders-section and hide positions-section
    personalInformationSection.style.display = "block";
    personalSecuritySection.style.display = "none";
    // cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";
    accountOverviewSection.style.display="block";


    // Highlight the clicked tab
    resetTabs();
    personalInformationTab.classList.add("active");
  });

  // Add event listener to positions-tab
  personalSecurityTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and show positions-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "block";
    // cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";
    accountOverviewSection.style.display="block";


    // Highlight the clicked tab
    resetTabs();
    personalSecurityTab.classList.add("active");
  });

  // Add event listener to fills-tab
  // cardInformationTab.addEventListener("click", function (event) {
  //   event.preventDefault();

  //   // Hide orders-section and positions-section and show fills-section
  //   personalInformationSection.style.display = "none";
  //   personalSecuritySection.style.display = "none";
  //   cardInformationSection.style.display = "block";
  //   balanceSection.style.display = "none";
  //   // activitySection.style.display = "none";
    // accountPageSection.style.display ='block';


  //   // Highlight the clicked tab
  //   resetTabs();
  //   cardInformationTab.classList.add("active");
  // });

  balanceTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    // cardInformationSection.style.display = "none";
    balanceSection.style.display = "block";
    activitySection.style.display = "none";
    accountOverviewSection.style.display="block";


    // Highlight the clicked tab
    resetTabs();
    balanceTab.classList.add("active");
  });

  activityTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    // cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "block";
    accountOverviewSection.style.display="none";
    accountPageSection.style.display ='block';


    // Highlight the clicked tab
    resetTabs();
    activityTab.classList.add("active");
  });
});

