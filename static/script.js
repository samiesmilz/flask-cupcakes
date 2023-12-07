// sending an api request
const BASE_URL = "http://127.0.0.1:5000/api/cupcakes";

async function getCupcakes() {
  try {
    const result = await axios.get(BASE_URL);
    const cupcakes = result.data.cupcakes;

    $("li").remove();
    // Use for...of loop to iterate over cupcakes array
    for (let cake of cupcakes) {
      const newLi = $("<li>");
      const flavor = cake.flavor;
      const span = $("<span>");
      span.text(flavor);
      const removeBtn = $("<button>");
      removeBtn.attr("id", cake.id);
      removeBtn.text("remove").addClass("btn btn-sm btn-warning ms-1 delete");
      newLi.append(span);
      newLi.append(removeBtn);
      newLi.addClass("p-1 bg-warning-subtle list-group-item ");
      $(".cupcakes").append(newLi);
    }
  } catch (error) {
    console.error("Error fetching cupcakes:", error);
  }
}

$("#show_cupcakes").on("click", function () {
  getCupcakes();
});

async function createCupcake() {
  try {
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();

    // Validation
    if (!flavor || !size || !rating || !image) {
      console.error("Please fill in all the required fields.");
      return;
    }

    // Loading indicator
    $("#create_cake_btn").prop("disabled", true);
    $("#loading_indicator").show();

    const newCake = { flavor, size, rating, image };
    const newCakeJSON = JSON.stringify(newCake);
    const res = await axios.post(BASE_URL, newCakeJSON, {
      headers: { "Content-Type": "application/json" },
    });

    // Hide loading indicator
    $("#create_cake_btn").prop("disabled", false);
    $("#loading_indicator").hide();

    $("#flavor").val("");
    $("#size").val("");
    $("#rating").val("");
    $("#image").val("");

    // Response handling
    if (res.status === 201) {
      // Update UI or show confirmation message
    } else {
      console.error("Error creating cupcake:", res.statusText);
    }
  } catch (error) {
    console.error("Error creating a cupcake:", error, error.response?.status);
  }
}

$("#create_cake_btn").on("click", async function () {
  await createCupcake();
  getCupcakes();
});

async function deleteCake() {
  const id = $(this).attr("id");
  const res = await axios.delete(`${BASE_URL}/${id}`);
  $(this).parent().remove();
  getCupcakes();
}

$(".cupcakes").on("click", ".delete", deleteCake);
