document.addEventListener("DOMContentLoaded", () => {
  const predictionForm = document.querySelector("form[action='/predict/api/predict']");

  if (predictionForm) {
    predictionForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(predictionForm);
      const imageFile = formData.get("image");
      const plantType = formData.get("plant_type");
      const location = formData.get("location");
      const date = formData.get("date");

      // ✅ Basic form validation
      if (!plantType || !location || !date) {
        alert("Please fill in all fields: Plant Type, Location, and Date.");
        return;
      }

      // ✅ Client-side image validation
      if (!imageFile || !imageFile.type.startsWith("image/")) {
        alert("Please upload a valid image file (JPG or PNG).");
        return;
      }

      // ✅ Read image as base64 and store it for preview
      const reader = new FileReader();
      reader.onload = async () => {
        sessionStorage.setItem("uploadedImage", reader.result);  // store base64 image

        try {
          // ✅ Send form data to the backend
          const response = await fetch("/predict/api/predict", {
            method: "POST",
            body: formData
          });

          const result = await response.json();

          if (response.ok) {
            // ✅ Store prediction result and redirect
            sessionStorage.setItem("prediction_result", JSON.stringify(result));
            window.location.href = "result.html";
          } else {
            // ❌ Handle backend errors
            alert(result.message || "Prediction failed due to server error.");
            console.error("Server error:", result);
          }
        } catch (error) {
          alert("Error sending prediction request. Please try again.");
          console.error("Request error:", error);
        }
      };

      reader.readAsDataURL(imageFile);  // triggers reader.onload
    });
  }
});
