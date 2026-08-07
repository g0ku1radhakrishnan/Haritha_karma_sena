Haritha karma sena



The "Haritha Karma Sena" (HKS) system is a comprehensive web-based platform designed to facilitate efficient waste management and environmental stewardship in local communities. The system is divided into four main user categories: administrators, public/users, HKS members, and IT officers, each with specific functionalities and roles.

Administrators have the authority to log in and oversee various aspects of the system, including managing wards, HKS members, and IT officers. They can assign HKS members to specific wards, manage IT officer details, and monitor complaints from both HKS members and users. Furthermore, administrators have the capability to view user profiles.

Public/users can register and log in to the system, enabling them to report their waste contributions, file complaints, and view responses. They can also browse and purchase recycled products, categorized as either bio or plastic, and manage their shopping carts, payments, and order histories. Users can send custom waste requests, track their statuses, and receive notifications from IT officers and HKS members. Additionally, users can report public waste issues with images and location details and keep track of their rewards.

HKS members have distinct functionalities based on their roles: "A" for normal waste management, "B" for custom waste requests, and "C" for delivery management. They can log in, file complaints to IT officers, view responses, manage waste in their assigned wards, verify waste, and receive notifications from IT officers. Custom waste request handlers can view and update custom waste requests, while delivery managers can oversee orders and update delivery and payment confirmation details.

IT officers play a pivotal role in the system, as they can log in, send notifications to HKS members and users, manage complaints, and provide responses. They are responsible for maintaining product information, waste reports, payment histories, and interacting with HKS members and users.

The system's database consists of several interconnected tables, such as login, user, HKS, IT officer, ward, assignment records, complaints, waste records, product details, order records, payment records, notifications, custom waste requests, custom waste statuses, public waste reports, and reward records.

In summary, the "Haritha Karma Sena" system is a comprehensive waste management platform that empowers users, HKS members, administrators, and IT officers to collaboratively address waste-related issues, purchase recycled products, and promote environmental sustainability within their communities.

	admin
	login
	manage ward
	manage hks
	assign to ward
	manage it_officer
	view complaints( hks/users  )
	view users


	public/user
	register
	login
	add my waste
	send complaints
	view reply
	view recycle product
	bio
	plastic
	add to cart
	view my cart
	make payments redeem reward points
	view my order history
	view notifications from it
	view notifications from hks	
	send custom waste request
	view custom waste request and status
	make payment
	send public waste details( with images and location )
	view my reward


	hks
	login
	send complaints to it
	view reply
	A( Normal )
	send notifications to users
	view notifications from it
	view waste	
	update status

	B( custom )
	view custom waste request
	update status
	view public waste
		verify waste
	view notifications from it
	C( delivery )
	view order
	update delivery details
	update payment confirmation




	it officer
	login
	send notification to hks/users
	view complaints( hks/users  )
	send reply
	manage products
	bio
	plastic
	waste report	
	payment history
	view hks



Tables

	login
	login_id
	username
	password
	usertype

	user
	user_id
	login_id
	ward_id
	building_owner_name
	building_number
	housename
	place
	phone
	email

	hks
	hks_id
	login_id
	name
	place
	phone
	email
	type(normal/custom/delivery)


	it_officer
	officer_id
	login_id
	name
	phone
	email

	ward
	ward_id
	ward_number





	assign_ward
	assign_id
	hks_id
	ward_id


	complaints
	complaints_id
	sender_id(hks-login_id/user-login_id)
	receiver_id(it officer-login_id)
	description
	reply
	date

	my_waste
	my_waste_id
	user_id
	date
	status


	products
	products_id
	product_type(bio/plastic)
	product_name
	description
	image
	stock
	amount


	order_master
	om_id
	user_id
	total_amount
	date
	status

	order_child
	oc_id
	om_id
	product_id
	quantity
	amount

	od_payment
	od_payment_id
	om_id
	amount
	date
	status

	cust_payment
	cust_payment_id
	custom_waste_request_id
	amount
	date
	status



	it_notification
	it_notification_id
	title
	description
	date

	hks_notification
	hks_notification_id
	hks_id
	title
	description
	date

	custom_waste_request
	custom_waste_request_id
	user_id
	date
	total_amount
	status

	custom_waste_status
	custom_waste_status_id
	custom_waste_request_id
	plastic_quantity
	plastic_amount
	bio_quantity
	bio_amount


	public_waste
	public_waste_id
	user_id
	title
	latitude
	longitude
	image
	status


	rewards
	rewards_id
	public_waste_id
	rewards
	date


