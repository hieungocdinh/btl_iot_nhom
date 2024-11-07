let myPieChart = null;


document.addEventListener("DOMContentLoaded", function () {
    const selectElement = document.getElementById("trash-can-select");
    fetchTrashCanData();
    selectElement.addEventListener("change", fetchTrashCanData);
});

function fetchTrashCanData() {
    console.log("Fetching trash data...");
    const selectElement = document.getElementById("trash-can-select");
    const selectedTrashCanId = selectElement.value;

    fetch(`/api/trash-data/${selectedTrashCanId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Xử lý dữ liệu nhận được
            const trashCompartmentSelect = document.getElementById("trash-compartment-select");
            const trashDataContainer = document.getElementById("trash-data-container");

            // Làm sạch dữ liệu cũ
            trashDataContainer.innerHTML = "";
            trashCompartmentSelect.innerHTML = "";

            // Cập nhật progess section
            fetchProgessSection(selectedTrashCanId);

            // Thêm các tùy chọn ngăn rác (trash compartments)
            const optionAll = document.createElement("option");
            optionAll.value = "all";
            optionAll.textContent = "all";
            trashCompartmentSelect.appendChild(optionAll);
            data.trash_compartment.forEach(trashCompartment => {
                const option = document.createElement("option");
                option.value = trashCompartment.id;
                option.textContent = trashCompartment.lable;
                trashCompartmentSelect.appendChild(option);
            });

            // Thêm các mục rác (trash items) vào container
            data.trash_data.forEach(trash => {
                const img = document.createElement("img");

                // Đặt thuộc tính cho thẻ img dựa trên dữ liệu trả về
                img.src = trash.trash_img_url ? trash.trash_img_url : 'https://via.placeholder.com/100';
                img.alt = `${trash.label}`;
                img.dataset.date = trash.date;
                img.dataset.trashCompartmentId = trash.id_trash_compartment;

                trashDataContainer.appendChild(img);
            });

            fetchChartSection(selectedTrashCanId);
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
        });
}


function filterTrash() {
    const selectedCompartment = document.getElementById("trash-compartment-select").value;
    const trashDataContainer = document.getElementById("trash-data-container");
    const trashImages = trashDataContainer.getElementsByTagName("img");

    // Hiển thị lại tất cả hình ảnh
    for (let img of trashImages) {
        img.style.display = "block"; // Hiển thị lại tất cả hình ảnh
    }

    // Nếu không phải "all", lọc theo ID ngăn rác
    if (selectedCompartment !== "all" && selectedCompartment !== "other") {
        for (let img of trashImages) {
            if (img.dataset.trashCompartmentId !== selectedCompartment) {
                img.style.display = "none"; // Ẩn hình ảnh không khớp
            }
        }
    }
}


function fetchProgessSection(selectedTrashCanId) {
    const progessBarGroup = document.getElementById("progress-bar-group");

    fetch(`/api/trash-can-progress/${selectedTrashCanId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Xóa các phần tử cũ trong nhóm thanh tiến độ
            progessBarGroup.innerHTML = "";

            // Duyệt qua từng TrashCompartment và tạo thanh tiến độ
            data.trash_compartments.forEach(compartment => {
                // Tạo div chứa thanh tiến độ
                const progessBar = document.createElement("div");
                progessBar.className = "progress-bar";

                // Tạo nhãn cho thanh tiến độ (label)
                const label = document.createElement("label");
                label.textContent = `${compartment.label} :`;  // label từ TrashCompartment (Battery, Plastic, etc.)

                // Tạo thanh bar
                const bar = document.createElement("div");
                bar.className = "bar";

                // Tạo phần fill của thanh tiến độ
                const fill = document.createElement("div");
                fill.className = "fill";
                fill.style.width = `${compartment.percentage}%`;  // Tỷ lệ phần trăm từ dữ liệu API

                // Tạo phần text hiển thị giữa thanh tiến độ
                const progressText = document.createElement("span");
                progressText.className = "progress-text";
                progressText.textContent = `${compartment.total_quantity}/${compartment.max_quantity}`;  // Hiển thị số lượng hiện tại và tối đa

                // Gắn phần text vào phần fill
                fill.appendChild(progressText);

                // Gắn phần fill vào bar
                bar.appendChild(fill);

                // Tạo nút "Đặt lại"
                const resetButton = document.createElement("button");
                resetButton.className = "reset";
                resetButton.textContent = "Đặt lại";
                resetButton.addEventListener("click", function () {
                    // Gửi yêu cầu đặt lại thông qua API
                    fetch(`/api/reset-progress/${compartment.id}`)
                        .then(response => response.json())  // Chuyển đổi phản hồi thành JSON
                        .then(data => {
                            if (data.status === 'success') {
                                // Nếu phản hồi là thành công, reload trang
                                window.location.reload();
                            } else {
                                // Nếu có lỗi, bạn có thể hiển thị thông báo lỗi
                                console.error('Error resetting progress:', data.message);
                            }
                        })
                        .catch(error => {
                            console.error("Error resetting progress:", error);
                        });
                });

                // Gắn nhãn, bar và nút vào thanh tiến độ
                progessBar.appendChild(label);
                progessBar.appendChild(bar);
                progessBar.appendChild(resetButton);

                // Gắn thanh tiến độ vào nhóm thanh tiến độ
                progessBarGroup.appendChild(progessBar);
            });
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
        });
}

function fetchChartSection(trashCanId) {
    fetch(`/api/get-trash-data-to-chart/${trashCanId}`)
        .then(response => response.json())
        .then(data => {
            const labels = data.labels;
            const chartData = data.data;

            // Kiểm tra và hủy biểu đồ cũ nếu có
            if (myPieChart) {
                myPieChart.destroy();
            }

            // Khởi tạo biểu đồ với dữ liệu nhận từ API
            const ctx = document.getElementById("chart-section-pie");
            myPieChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Số lượng rác',
                        data: chartData,  // Dữ liệu số lượng rác
                        backgroundColor: [
                            '#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0',
                            '#ffb3e6', '#b3e6ff', '#ffccff', '#c2f0c2', '#ffb366'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    var total = tooltipItem.dataset.data.reduce((acc, val) => acc + val, 0);
                                    var currentValue = tooltipItem.raw;
                                    var percentage = Math.round((currentValue / total) * 100);
                                    return tooltipItem.label + ': ' + currentValue + ' (' + percentage + '%)';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}