export default function GoogleLoginButton() {
    const handleGoogleLogin = () => {
      console.log("Google Login Clicked");
    };
  
    return (
      <button onClick={handleGoogleLogin}>
        Continue with Google
      </button>
    );
  }