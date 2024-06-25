import defaultSettings from '../../src/settings'

const title = defaultSettings.title || 'chinabidding'

export function getPageTitle(pageTitle) {
    if (pageTitle) {
        return `${pageTitle} - ${title}`
    }
    return `${title}`
}
