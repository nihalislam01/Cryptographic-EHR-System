import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import AuthContext from "../contexts/authContext";

export default function Login() {

    const navigate = useNavigate();
    const { login } = useContext(AuthContext);
    const [formData, setFormData] = useState({
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

    const onSubmitHandler = async (e) => {
        e.preventDefault();
        try {
            await login(formData);
            navigate("/dashboard");
        } catch (error) {
            console.error(error.response?.data || 'Login error');
        }
    }
    
    return (
        <>
            <Navbar />
            <div className="d-flex justify-content-center align-items-center w-100" style={{ minHeight: "90vh" }}>
                <div className="d-flex flex-column border gap-2" style={{width: "500px", padding: "20px", boxShadow: "5px 5px 12px 1px rgba(171, 171, 171, 0.41)"}}>
                    <h4>Login</h4>
                    <hr />
                    <input type="email" name="email" placeholder="Enter Email" onChange={onChangeHandler} />
                    <input type="password" name="password" placeholder="Enter Password" onChange={onChangeHandler} />
                    <hr />
                    <button className="w-100" onClick={onSubmitHandler}>Login</button>
                    <Link to="/register" className="btn btn-link">Don't have an account? signup here</Link>
                </div>
            </div>
        </>
    )
}