'use strict'; // Enables strict mode, read here for more details: https://stackoverflow.com/questions/1335851/what-does-use-strict-do-in-javascript-and-what-is-the-reasoning-behind-it

let formsNeedingValidation = document.querySelectorAll('.needs-validation'); 

formsNeedingValidation = Array.from(formsNeedingValidation);

// This function checks each invidvidual form to see if they are valid.
function checkIndividualForm (event){
    let currentForm = event.target;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value; 

    if(!currentForm.checkValidity()){
        event.preventDefault();
        event.stopPropagation();
    }

    if(password !== confirmPassword){
        event.preventDefault();
        event.stopPropagation();
        document.getElementById("confirmPassword").setCustomValidity("Passwords must match!");
    }
    else{
        document.getElementById("confirmPassword").setCustomValidity("");
    }

    currentForm.classList.add('was-validated');

    return;
}

// This functions loops through all the forms and individually passes them into the checkIndividualForm function. 
// Then it checks to see if the password and confirmPassword are both the same before allowing the form to be submitted.
function formsValidation (forms){
    forms.forEach(function(currentForm){
        currentForm.addEventListener('submit', checkIndividualForm, false);
    })

    if(password != confirmPassword){
        forms.event.preventDefault();
        forms.event.stopPropagation();
    }

    return;
}

formsValidation(formsNeedingValidation);