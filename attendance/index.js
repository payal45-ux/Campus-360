const { createRoot } = ReactDOM;
const { useEffect, useState } = React;

const App = () => {
    const [user, setUser ] = useState('');
    const io = new faceIO('your_public_key');

    const register = () => {
        io.enroll({ "locale": "auto", "payload": { UID: Date.now() } })
            .then(userInfo => {
                alert(`User  Successfully Enrolled! Details: Unique Facial ID: ${userInfo.facialId}`);
            })
            .catch(errCode => {
                console.log(errCode);
            });
    };

    const login = () => {
        io.authenticate({ "locale": "auto" })
            .then(userData => {
                console.log("Success, user identified");
                setUser (userData.payload.UID);
            })
            .catch(errCode => {
                console.log(errCode);
            });
    };

    const logout = () => {
        setUser ('');
        window.location.reload();
    };

    return (
        <div className="app">
            <h1>Face Recognition App</h1>
            {!user ? (
                <>
                    <button onClick={register}>Register</button>
                    <button onClick={login}>Login</button>
                </>
            ) : (
                <div className="notice">
                    <h2>Welcome Back!</h2>
                    <p>Your unique ID: {user}</p>
                    <button onClick={logout}>Logout</button>
                </div>
            )}
        </div>
    );
};

const root = createRoot(document.getElementById('root'));
root.render(<App />);