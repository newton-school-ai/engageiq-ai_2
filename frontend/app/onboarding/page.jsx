export default function Onboarding() {
    return (
      <div>
        <h1>Onboarding</h1>
  
        <label>Role</label>
        <select>
          <option>Student</option>
          <option>Teacher</option>
        </select>
  
        <br /><br />
  
        <label>Privacy</label>
        <select>
          <option>Local Only</option>
          <option>Share with Teacher</option>
        </select>
  
        <br /><br />
  
        <button>Continue</button>
      </div>
    );
  }