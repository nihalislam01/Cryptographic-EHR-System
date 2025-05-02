import { useState } from "react";
import { Link } from "react-router-dom";

export default function Register() {

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });

    const onChangeHandler = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const onSubmitHandler = (e) => {
        e.preventDefault();
        console.log(formData);
    }
    
    return (
        <div className="d-flex justify-content-center align-items-center w-100 min-vh-100">
            <div className="d-flex flex-column border gap-2" style={{width: "500px", padding: "20px", boxShadow: "5px 5px 12px 1px rgba(171, 171, 171, 0.41)"}}>
                <h4>Register</h4>
                <hr />
                <input type="text" name="username" placeholder="Enter Name" onChange={onChangeHandler} />
                <input type="email" name="email" placeholder="Enter Email" onChange={onChangeHandler} />
                <input type="password" name="password" placeholder="Enter Password" onChange={onChangeHandler} />
                <hr />
                <button className="w-100" onClick={onSubmitHandler}>Sign Up</button>
                <Link to="/" className="btn btn-link">Already registered? login here</Link>
            </div>
        </div>
    )
}