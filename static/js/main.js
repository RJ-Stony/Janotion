document.addEventListener("DOMContentLoaded", function () {
  // 테이블의 행을 드래그하여 재정렬할 수 있는 기능
  const taskTables = document.querySelectorAll(".task-table");

  if (taskTables.length > 0) {
    taskTables.forEach((table) => {
      const tbody = table.querySelector("tbody");
      if (tbody) {
        new Sortable(tbody, {
          animation: 150,
          handle: ".drag-handle",
          onEnd: function (evt) {
            const taskId = evt.item.dataset.taskId;
            const newPosition = evt.newIndex;

            // 서버에 순서 변경을 알리는 AJAX 요청
            // 여기에 구현이 필요합니다
          },
        });
      }
    });
  }

  // 프로그레스 바 상호작용
  const progressInputs = document.querySelectorAll(
    'input[type="range"].progress-control'
  );
  if (progressInputs.length > 0) {
    progressInputs.forEach((input) => {
      const progressBar = document.querySelector(
        `#progress-bar-${input.dataset.taskId}`
      );
      const progressValue = document.querySelector(
        `#progress-value-${input.dataset.taskId}`
      );

      input.addEventListener("input", function () {
        const value = this.value;
        progressBar.style.width = `${value}%`;
        progressValue.textContent = `${value}%`;
      });
    });
  }

  // 애니메이션 설정
  const animationElements = document.querySelectorAll(
    ".board-card, .task-item, .project-header, .project-content"
  );

  // 스크롤 애니메이션
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }
      });
    },
    { threshold: 0.1 }
  );

  animationElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    observer.observe(el);
  });

  // 드래그 앤 드롭 기능 (Sortable.js가 필요)
  if (typeof Sortable !== "undefined") {
    // 보드 내 카드 정렬
    document.querySelectorAll(".board-cards").forEach((el) => {
      Sortable.create(el, {
        animation: 150,
        ghostClass: "sortable-ghost",
        chosenClass: "sortable-chosen",
        dragClass: "sortable-drag",
        group: "tasks",
        onEnd: function (evt) {
          // 서버에 상태 변경을 알리는 AJAX 요청
          const taskId = evt.item.dataset.taskId;
          const newStatus = evt.to.closest(".board-column").dataset.status;
          const url = `/api/update-task-status/${taskId}/`;

          fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ status: newStatus }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                showNotification("작업 상태가 변경되었습니다", "success");
              } else {
                showNotification("오류가 발생했습니다", "error");
              }
            });
        },
      });
    });
  }

  // 뷰 전환 탭
  document.querySelectorAll(".view-tab").forEach((tab) => {
    tab.addEventListener("click", function () {
      const viewType = this.dataset.view;

      // 활성 탭 표시
      document
        .querySelectorAll(".view-tab")
        .forEach((t) => t.classList.remove("active"));
      this.classList.add("active");

      // 뷰 전환
      document.querySelectorAll(".view-content").forEach((view) => {
        view.style.display = "none";
      });
      document.getElementById(`${viewType}-view`).style.display = "block";

      // 애니메이션 재실행
      setTimeout(() => {
        const elements = document.querySelectorAll(
          `#${viewType}-view .board-card, #${viewType}-view .task-item`
        );
        elements.forEach((el, index) => {
          el.style.opacity = "0";
          el.style.transform = "translateY(20px)";

          setTimeout(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
          }, index * 50);
        });
      }, 50);
    });
  });

  // 체크박스 애니메이션
  document
    .querySelectorAll('.task-checkbox input[type="checkbox"]')
    .forEach((checkbox) => {
      checkbox.addEventListener("change", function () {
        const taskItem = this.closest(".task-item");
        if (this.checked) {
          taskItem.style.opacity = "0.7";
        } else {
          taskItem.style.opacity = "1";
        }
      });
    });

  // 토글 사이드바
  const sidebarToggle = document.querySelector(".sidebar-toggle");
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", function () {
      const sidebar = document.querySelector(".sidebar");
      sidebar.classList.toggle("collapsed");
    });
  }

  // CSRF 토큰 가져오기
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // 알림 메시지 표시
  function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.opacity = "1";
      notification.style.transform = "translateY(0)";
    }, 10);

    setTimeout(() => {
      notification.style.opacity = "0";
      notification.style.transform = "translateY(-20px)";

      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 3000);
  }

  // 호버 효과
  const hoverElements = document.querySelectorAll(
    ".board-card, .sidebar-item, .btn-action, .btn-icon"
  );
  hoverElements.forEach((el) => {
    el.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-2px)";
    });

    el.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });
});

// 모바일 메뉴 토글
document.addEventListener("DOMContentLoaded", function () {
  const mobileMenuToggle = document.querySelector(".mobile-menu-toggle");
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", function () {
      const sidebar = document.querySelector(".sidebar");
      sidebar.classList.toggle("sidebar-mobile-open");
    });
  }
});
