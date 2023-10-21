// Generated file; do not edit. See `schema-gen` crate.

use crate::prelude::*;

use super::brand::Brand;
use super::contact_point::ContactPoint;
use super::image_object::ImageObject;
use super::organization_or_person::OrganizationOrPerson;
use super::postal_address_or_string::PostalAddressOrString;
use super::property_value_or_string::PropertyValueOrString;
use super::string::String;
use super::text::Text;

/// An organization such as a school, NGO, corporation, club, etc.
#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, WriteNode, ReadNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
#[derive(derive_more::Display)]
#[display(fmt = "Organization")]
#[jats(elem = "institution")]
pub struct Organization {
    /// The type of this item.
    pub r#type: MustBe!("Organization"),

    /// The identifier for this item.
    #[strip(metadata)]
    #[html(attr = "id")]
    pub id: Option<String>,

    /// Non-core optional fields
    #[serde(flatten)]
    #[html(flatten)]
    #[jats(flatten)]
    #[markdown(flatten)]
    pub options: Box<OrganizationOptions>,
}

#[skip_serializing_none]
#[derive(Debug, SmartDefault, Clone, PartialEq, Serialize, Deserialize, StripNode, HtmlCodec, JatsCodec, MarkdownCodec, TextCodec, WriteNode, ReadNode)]
#[serde(rename_all = "camelCase", crate = "common::serde")]
pub struct OrganizationOptions {
    /// Alternate names (aliases) for the item.
    #[strip(metadata)]
    pub alternate_names: Option<Vec<String>>,

    /// A description of the item.
    #[strip(metadata)]
    pub description: Option<Text>,

    /// Any kind of identifier for any kind of Thing.
    #[strip(metadata)]
    pub identifiers: Option<Vec<PropertyValueOrString>>,

    /// Images of the item.
    #[strip(metadata)]
    pub images: Option<Vec<ImageObject>>,

    /// The name of the item.
    #[strip(metadata)]
    pub name: Option<String>,

    /// The URL of the item.
    #[strip(metadata)]
    pub url: Option<String>,

    /// Postal address for the organization.
    pub address: Option<PostalAddressOrString>,

    /// Brands that the organization is connected with.
    pub brands: Option<Vec<Brand>>,

    /// Correspondence/Contact points for the organization.
    pub contact_points: Option<Vec<ContactPoint>>,

    /// Departments within the organization. For example, Department of Computer Science, Research & Development etc.
    pub departments: Option<Vec<Organization>>,

    /// Organization(s) or person(s) funding the organization.
    pub funders: Option<Vec<OrganizationOrPerson>>,

    /// The official name of the organization, e.g. the registered company name.
    pub legal_name: Option<String>,

    /// The logo of the organization.
    pub logo: Option<ImageObject>,

    /// Person(s) or organization(s) who are members of this organization.
    pub members: Option<Vec<OrganizationOrPerson>>,

    /// Entity that the Organization is a part of. For example, parentOrganization to a department is a university.
    pub parent_organization: Option<Organization>,
}

impl Organization {
    pub fn new() -> Self {
        Self {
            ..Default::default()
        }
    }
}
