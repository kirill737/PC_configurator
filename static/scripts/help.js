export async function getCurrentData() {
    console.log("<getCurrentData>")
    const response = await fetch(`/get/current/data`);
    const data = await response.json();
    console.log(data)
    return data;
}

export async function getCurrentCT() {
    console.log("<getCurrentCt>")

    const response = await fetch(`/get/current/data/ct`);

    const data = await response.json();

    return data['ct'];
}

export async function getCurrentBuildId() {
    console.log("<getCurrentBuildId>")
    const response = await fetch(`/get/current/data/build_id`);
    const data = await response.json();
    console.log(data)
    return data;
}

export async function setCurrentBuildId(build_id) {
    console.log("<setCurrentBuildId>")
    console.log("Текущий build id изменён на: " + build_id)
    const response = await fetch("/set/current/data/build_id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'build_id': build_id
        })
    });
}

export async function setCurrentCT(ct) {
    console.log("<setCurrentCT>")
    console.log("Текущий тип изменён на: " + ct)
    const response = await fetch("/set/current/data/ct", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'ct': ct
        })
    });
}

export async function updateBuildComponent(build_id, old_componment_id, new_component_id) {
    const response = await fetch("/change/build/component", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'build_id': build_id,
            'old_id': old_componment_id,
            'new_id': new_component_id
        })
    });
    console.log({
        'build_id': build_id,
        'old_id': old_componment_id,
        'new_id': new_component_id
    })
}

export async function translate(name, capitalize = true) {
    const response = await fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'name': name,
            'capitalize': capitalize
        })
    });
    const data = await response.json(); // дождаться JSON
    const translated_name = data.result; // получить нужное поле

    return translated_name;
}
