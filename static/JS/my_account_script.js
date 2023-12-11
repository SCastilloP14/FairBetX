document.addEventListener("DOMContentLoaded", function () {
    // Tabs 
  const personalInformationTab = document.getElementById("personal-information-tab");
  const personalSecurityTab = document.getElementById("personal-security-tab");
  const cardInformationTab = document.getElementById("card-information-tab");
  const addCreditCardTab = document.getElementById("add-credit-card-tab");
  const balanceTab = document.getElementById("balance-tab");
  const activityTab = document.getElementById("activity-tab");

    // Section 
  const personalInformationSection = document.getElementById("personal-information-section");
  const personalSecuritySection = document.getElementById("personal-security-section");
  const cardInformationSection = document.getElementById("card-information-section");
  const cardInformationOverviewSection = document.getElementById("card-information-overview-section");
  const balanceSection = document.getElementById("balance-section");
  const activitySection = document.getElementById("activity-section");
  const accountOverviewSection = document.getElementById("account-overview-section");
  const accountPageSection = document.getElementById("account-page-section");

  // Tab2 for activity Page 
  const activityPersonalInformationTab =  document.getElementById("activity-personal-information-tab");
  const activityPersonalSecurityTab =  document.getElementById("activity-personal-security-tab");
  const activityCardInformationTab =  document.getElementById("activity-card-information-tab");
  const activityBalanceTab =  document.getElementById("activity-balance-tab");

  // Function to remove "active" class from all tabs
  function resetTabs() {
    personalInformationTab.classList.remove("active");
    personalSecurityTab.classList.remove("active");
    cardInformationTab.classList.remove("active");
    balanceTab.classList.remove("active");
    activityTab.classList.remove("active");
    addCreditCardTab.classList.remove("active");
  }

  // Show orders-section by default and hide positions-section
  personalInformationSection.style.display = "block";
  personalSecuritySection.style.display = "none";
  cardInformationOverviewSection.style.display = "none";
  cardInformationSection.style.display = "none";
  balanceSection.style.display = "none";
  activitySection.style.display = "none";
  accountOverviewSection.style.display="block";



  // Add event listener to orders-tab
  personalInformationTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Show orders-section and hide positions-section
    personalInformationSection.style.display = "block";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
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
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";
    accountOverviewSection.style.display="block";


    // Highlight the clicked tab
    resetTabs();
    personalSecurityTab.classList.add("active");
  });

  // Add event listener to fills-tab
  cardInformationTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "block";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";
    accountOverviewSection.style.display="block";


    // Highlight the clicked tab
    resetTabs();
    cardInformationTab.classList.add("active");
  });

   // Add event listener to Credit card Overview-tab
  addCreditCardTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "block";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";
    accountOverviewSection.style.display="block";


    // Highlight the clicked tab
    resetTabs();
    addCreditCardTab.classList.add("active");
  });

  balanceTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
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
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "block";

    accountOverviewSection.style.display="none";
    accountPageSection.style.display ='block';


    // Highlight the clicked tab
    resetTabs();
    activityTab.classList.add("active");
  });

  // Activity Nav Bar 
  activityPersonalInformationTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "block";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";

    accountOverviewSection.style.display="block";
    accountPageSection.style.display ='flex';


    // Highlight the clicked tab
    resetTabs();
    activityPersonalInformationTab.classList.add("active");
  });
  activityPersonalSecurityTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "block";
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";

    accountOverviewSection.style.display="block";
    accountPageSection.style.display ='flex';


    // Highlight the clicked tab
    resetTabs();
    activityPersonalSecurityTab.classList.add("active");
  });

  activityCardInformationTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "block";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "none";
    activitySection.style.display = "none";

    accountOverviewSection.style.display="block";
    accountPageSection.style.display ='flex';


    // Highlight the clicked tab
    resetTabs();
    activityCardInformationTab.classList.add("active");
  });

   activityBalanceTab.addEventListener("click", function (event) {
    event.preventDefault();

    // Hide orders-section and positions-section and show fills-section
    personalInformationSection.style.display = "none";
    personalSecuritySection.style.display = "none";
    cardInformationOverviewSection.style.display = "none";
    cardInformationSection.style.display = "none";
    balanceSection.style.display = "block";
    activitySection.style.display = "none";

    accountOverviewSection.style.display="block";
    accountPageSection.style.display ='flex';


    // Highlight the clicked tab
    resetTabs();
    activityBalanceTab.classList.add("active");
  });


});

