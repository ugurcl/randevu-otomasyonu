const username = document.querySelector('#id_username');
const first_name = document.querySelector('#id_first_name');
const last_name = document.querySelector('#id_last_name')
const email = document.querySelector('#id_email')
const password = document.querySelector('#id_password1')
const rePassword = document.querySelector('#id_password2')
const btn = document.querySelector('#register_btn');


change_input_value(username, /^[a-zA-Z0-9çÇğĞıİöÖşŞüÜ_-]+$/, min_length=3);
change_input_value(first_name, /^[a-zA-ZçÇğĞıİöÖşŞüÜ]+$/, min_length=3);
change_input_value(last_name, /^[a-zA-ZçÇğĞıİöÖşŞüÜ]+$/,min_length=3);
change_input_value(email, /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/);
change_input_value(password, /(?=.*[A-Za-zÇŞĞÜÖİçşğüöı])(?=.*\d)[A-Za-zÇŞĞÜÖİçşğüöı\d@$!%*?&_]{8,}$/, 8, true);
change_input_value(rePassword, /(?=.*[A-Za-zÇŞĞÜÖİçşğüöı])(?=.*\d)[A-Za-zÇŞĞÜÖİçşğüöı\d@$!%*?&_]{8,}$/, 8, true);

function validate_all_inputs() {
    return (
        username.classList.contains('validate_input') &&
        first_name.classList.contains('validate_input') &&
        last_name.classList.contains('validate_input') &&
        email.classList.contains('validate_input') &&
        password.classList.contains('validate_input') &&
        rePassword.classList.contains('validate_input')
    );
}

function change_input_value(input_name, regex_validation, min_length=null, is_Passwords=false) {
    let is_valid = false;
    input_name.addEventListener('input', function () {
        if (regex_validation.test(input_name.value)) {
            input_name.classList.add('validate_input');
            input_name.classList.remove('invalidate_input');
            is_valid = true;
        } else {
            input_name.classList.remove('validate_input');
            input_name.classList.add('invalidate_input');
            is_valid = false;
        }
        let value = this.value;
        if (value.length < min_length){
            input_name.classList.remove('validate_input');
            input_name.classList.add('invalidate_input');
            is_valid = false;
        }else {
            is_valid = true;
        }

        if(is_Passwords){
            if (password.value !== rePassword.value) {
                rePassword.classList.remove('validate_input');
                rePassword.classList.add('invalidate_input');
                is_valid = false;
            } else {
                rePassword.classList.add('validate_input');
                rePassword.classList.remove('invalidate_input');
                is_valid = true;
            }
        }

        if (is_valid && validate_all_inputs()) {
            btn.disabled = false;
        } else {
            btn.disabled = true;
        }
    });
 
}