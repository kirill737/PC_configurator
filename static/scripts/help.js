export async function getCurrentData() {
    const response = await fetch(`/get/current/component/data`);
    const data = await response.json();
    return data;
}

export async function setCurrentComponentDataBuildId(build_id) {
    const response = await fetch("/set/current/component/data/build_id", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'build_id': build_id
        })
    });
}

export async function setCurrentComponentDataCT(ct) {
    console.log("setCurrentComponentDataCT");
    const response = await fetch("/set/current/component/data/ct", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            'ct': ct
        })
    });
}

export async function updateBuildComponent(build_id, old_componment_id, new_component_id) {
    const response = await fetch("/update/build/component", {
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
