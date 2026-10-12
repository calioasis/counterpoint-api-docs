Redoc.init("openapi.json", {
  disableGoogleFont: true, hideDownloadButton: true, requiredPropsFirst: true,
  pathInMiddlePanel: true, expandResponses: "200,201", jsonSampleExpandLevel: 2,
  theme: {colors:{primary:{main:"#137864"}},typography:{fontSize:"15px",lineHeight:"1.65",fontFamily:"system-ui, sans-serif",headings:{fontFamily:"system-ui, sans-serif",fontWeight:"650"},code:{fontFamily:"ui-monospace, SFMono-Regular, monospace",fontSize:"13px"}},sidebar:{backgroundColor:"#f6f8fa",width:"265px"},rightPanel:{backgroundColor:"#173041"}}
}, document.getElementById("reference"));
