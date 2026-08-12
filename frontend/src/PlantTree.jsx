import { useEffect, useState } from "react";
import axios from "axios";

function PlantTree({ onBack }) {
  const [treeName, setTreeName] = useState("");
  const [locationId, setLocationId] = useState("");
  const [plantingDate, setPlantingDate] = useState("");
  const [locations, setLocations] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const getLocations = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/locations",
          {
            withCredentials: true,
          }
        );

        setLocations(response.data);
      } catch (error) {
        console.error(error);
        setMessage("Unable to load locations.");
      }
    };

    getLocations();
  }, []);

  const handlePlantTree = async (e) => {
    e.preventDefault();

    setMessage("");

    try {
      const formData = new URLSearchParams();

      formData.append("tree_name", treeName);
      formData.append("location_id", locationId);
      formData.append("planting_date", plantingDate);

      const response = await axios.post(
        "http://localhost:8000/plant-tree",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          withCredentials: true,
        }
      );

      setMessage(response.data.message);

      setTreeName("");
      setLocationId("");
      setPlantingDate("");
    } catch (error) {
      console.error(error);

      setMessage(
        error.response?.data?.message ||
        "Unable to plant tree."
      );
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <h1 className="text-success mb-4">
          🌱 Plant a Tree
        </h1>

        <form onSubmit={handlePlantTree}>

          <div className="mb-3">
            <label className="form-label">
              Tree Name
            </label>

            <input
              type="text"
              className="form-control"
              placeholder="Enter tree name"
              value={treeName}
              onChange={(e) => setTreeName(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">
              Plantation Location
            </label>

            <select
              className="form-select"
              value={locationId}
              onChange={(e) => setLocationId(e.target.value)}
              required
            >
              <option value="">
                Select location
              </option>

              {locations.map((location) => (
                <option
                  key={location.id}
                  value={location.id}
                >
                  {location.name}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-4">
            <label className="form-label">
              Planting Date
            </label>

            <input
              type="date"
              className="form-control"
              value={plantingDate}
              onChange={(e) => setPlantingDate(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-success"
          >
            🌳 Plant Tree
          </button>

        </form>

        {message && (
  <div className="alert alert-info mt-4">
    {message}
  </div>
)}

{message === "Tree planted successfully!" && (
  <button
    className="btn btn-primary mt-3"
    onClick={onBack}
  >
    ← Back to Dashboard
  </button>
)}
      </div>
    </div>
  );
}

export default PlantTree;