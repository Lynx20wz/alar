export default async function isAuthenticated() {
  const token = localStorage.getItem("auth_token");
  const username = localStorage.getItem("username");

  if (!token && !username) {
    window.location.href = "/login";
  }

  try {
    await fetch("/api/token", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  } catch (error) {
    window.location.href = "/login";
  }
}
