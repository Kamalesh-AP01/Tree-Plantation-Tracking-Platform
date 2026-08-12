import { useEffect, useState } from "react";
import PlantTree from "./PlantTree";
import PlantationRecords from "./PlantationRecords";
import axios from "axios";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");
  const [showPlantTree, setShowPlantTree] = useState(false);

  useEffect(() => {
    const getDashboard = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/dashboard",
          {
            withCredentials: true,
          }
        );

        setDashboard(response.data);
      } catch (error) {
        console.error(error);
        setError("Unable to load dashboard.");
      }
    };

    getDashboard();
  }, [showPlantTree]);

  if (error) {
    return <h2>{error}</h2>;
  }

  if (showPlantTree) {
    return (
      <PlantTree
        onBack={() => {
          setShowPlantTree(false);
        }}
      />
    );
  }

  if (!dashboard) {
    return <h2>Loading dashboard...</h2>;
  }

  return (
    <div style={{ padding: "40px" }}>

      <h1>Tree Plantation Tracking Platform</h1>

      <p>
        Welcome, <strong>{dashboard.user_name}</strong>
      </p>

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginTop: "30px",
        }}
      >

        <div className="card p-4">
          <h3>Trees Planted</h3>
          <p>{dashboard.trees_planted}</p>
        </div>

        <div className="card p-4">
          <h3>College Locations</h3>
          <p>{dashboard.total_locations}</p>
        </div>

        <div className="card p-4">
          <h3>Total Users</h3>
          <p>{dashboard.total_users}</p>
        </div>

      </div>

      <h2 className="mt-5">Plantation Locations</h2>

      <ul>
        <li>Backside Canteen</li>
        <li>PT Ground</li>
        <li>Backside Cafe</li>
        <li>Hostel Boys Area</li>
        <li>Hostel Girls Area</li>
      </ul>

      <PlantationRecords />

      <button
        className="btn btn-success mt-4"
        onClick={() => setShowPlantTree(true)}
      >
        🌱 Plant a Tree
      </button>

    </div>
  );
}

export default Dashboard;