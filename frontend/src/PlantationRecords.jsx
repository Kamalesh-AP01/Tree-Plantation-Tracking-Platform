import { useEffect, useState } from "react";
import axios from "axios";

function PlantationRecords() {
  const [plantations, setPlantations] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const getPlantations = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/plantations",
          {
            withCredentials: true,
          }
        );

        setPlantations(response.data.plantations);
      } catch (error) {
        console.error(error);
        setError("Unable to load plantation records.");
      }
    };

    getPlantations();
  }, []);

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="mt-5">
      <h2>🌳 Plantation Records</h2>

      {plantations.length === 0 ? (
        <p className="text-muted">
          No plantation records yet.
        </p>
      ) : (
        <table className="table table-bordered table-striped mt-3">
          <thead>
            <tr>
              <th>Tree</th>
              <th>Location</th>
              <th>Planting Date</th>
              <th>Planted By</th>
            </tr>
          </thead>

          <tbody>
            {plantations.map((record) => (
              <tr key={record.id}>
                <td>{record.tree_name}</td>
                <td>{record.location}</td>
                <td>{record.planting_date}</td>
                <td>{record.planted_by}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PlantationRecords;