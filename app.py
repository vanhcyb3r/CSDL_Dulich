import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from datetime import date
app = Flask(__name__)
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",  # Thay bằng mật khẩu của bạn
        database="qltourdulich"  # Thay bằng tên database của bạn
    )
    return connection
@app.route('/')
def trang_chu():
    return render_template('index.html')

@app.route('/tim-kiem-tour', methods=['GET'])
def danh_sach_tour():
    TourName = request.args.get('TourName', '')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Nếu có yêu cầu tìm kiếm, sử dụng LIKE để tìm theo tên
    if TourName:
        query = "SELECT * FROM Tour WHERE TourName LIKE %s"
        cursor.execute(query, ('%' + TourName + '%',))
    else:
        query = "SELECT * FROM Tour"
        cursor.execute(query)

    tours = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('list.html', tours=tours)

@app.route('/quan-ly-tour')
def quan_ly_tour():
    # Truy vấn và hiển thị danh sách tour
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Tour")
    tours = cursor.fetchall()
    
    conn.close()
    return render_template('manage_tour.html', tours=tours)
@app.route('/them-tour', methods=['GET', 'POST'])
def them_tour():
    if request.method == 'POST':
        TourID = request.form['TourID']
        TourName = request.form['TourName']
        AdminID = request.form['AdminID']
        Departure_Location = request.form['Departure_Location']
        Destination = request.form['Destination']
        Description = request.form['Description']
        Departure_date = request.form['Departure_date']
        Price = request.form['Price']
        Num_tickets = request.form['Num_tickets']

        # Kết nối tới cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()

        # Chèn dữ liệu mới vào bảng Tour
        cursor.execute("""
            INSERT INTO Tour (TourID, TourName, AdminID, Departure_Location, Destination, Description, Departure_date, Price, Num_tickets)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (TourID, TourName, AdminID, Departure_Location, Destination, Description, Departure_date, Price, Num_tickets))
        conn.commit()
        conn.close()

        # Sau khi thêm tour thành công, chuyển hướng về trang quản lý tour
        return redirect(url_for('quan_ly_tour'))

    return render_template('add_tour.html')
@app.route('/sua-tour/<int:TourID>', methods=['GET', 'POST'])
def sua_tour(TourID):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        TourName = request.form['TourName']
        Departure_Location = request.form['Departure_Location']
        Destination = request.form['Destination']
        Departure_date = request.form['Departure_date']
        Price = request.form['Price']
        Num_tickets = request.form['Num_tickets']

        # Cập nhật dữ liệu tour trong database
        cursor.execute("""
            UPDATE Tour
            SET TourName = %s, Departure_Location = %s, Destination = %s, Departure_date = %s, Price = %s, Num_tickets = %s
            WHERE TourID = %s
        """, (TourName, Departure_Location, Destination, Departure_date, Price, Num_tickets, TourID))

        conn.commit()
        conn.close()
        return redirect(url_for('quan_ly_tour'))

    # Lấy thông tin tour hiện tại từ database
    cursor.execute("SELECT * FROM Tour WHERE TourID = %s", (TourID,))
    tour = cursor.fetchone()
    conn.close()
    
    return render_template('edit_tour.html', tour=tour)
@app.route('/xoa-tour/<int:TourID>', methods=['POST'])
def xoa_tour(TourID):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Xóa tour dựa trên mã tour
        cursor.execute("DELETE FROM Tour WHERE TourID = %s", (TourID,))
        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback nếu có lỗi
        print(f"Lỗi: {e}")
    finally:
        conn.close()  # Đóng kết nối sau khi xóa

    # Quay lại trang quản lý tour
    return redirect(url_for('quan_ly_tour'))

@app.route('/quan-ly-khach-hang')
def quan_ly_khach_hang():
    conn = get_db_connection()  # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor(dictionary=True)  # Sử dụng dictionary cursor
    
    cursor.execute("SELECT * FROM User")  # Truy vấn tất cả khách hàng
    khach_hangs = cursor.fetchall()  # Lấy danh sách khách hàng

    conn.close()  # Đóng kết nối
    
    # Truyền danh sách khách hàng vào template
    return render_template('manage_khach_hang.html', khach_hangs=khach_hangs)

@app.route('/them-khach-hang', methods=['GET', 'POST'])
def them_khach_hang():
    if request.method == 'POST':
        UserID = request.form['UserID']
        Full_Name = request.form['Full_Name']
        ID_number = request.form['ID_number']
        IdType = request.form['IdType']
        Phone_number = request.form['Phone_number']
        Email = request.form['Email']
        Address = request.form['Address']
        AdminID = request.form['AdminID']
        # Kết nối đến cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()

        # Thêm khách hàng mới vào bảng User
        cursor.execute("""
            INSERT INTO User (UserID, Full_Name, ID_number, IdType, Phone_number, Email, Address, AdminID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (UserID, Full_Name, ID_number, IdType, Phone_number, Email, Address, AdminID))
        
        conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        conn.close()   # Đóng kết nối

        return redirect(url_for('quan_ly_khach_hang'))  # Quay lại trang quản lý khách hàng sau khi thêm

    # Hiển thị form nếu là phương thức GET
    return render_template('them_khach_hang.html')
@app.route('/thong-ke')
def thong_ke():
    conn = get_db_connection()  # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor(dictionary=True)  # Sử dụng dictionary cursor
    
    # Thống kê tổng doanh thu
    cursor.execute("SELECT SUM(Total) AS tong_doanh_thu FROM Invoice")
    tong_doanh_thu = cursor.fetchone()["tong_doanh_thu"]
    
    # Thống kê số lượng khách hàng
    cursor.execute("SELECT COUNT(UserID) AS so_luong_khach_hang FROM User")
    so_luong_khach_hang = cursor.fetchone()["so_luong_khach_hang"]
    
    # Thống kê số lượng tour đã được đặt
    cursor.execute("SELECT COUNT(DISTINCT TourID) AS so_luong_tour_da_dat FROM Invoice")
    so_luong_tour_da_dat = cursor.fetchone()["so_luong_tour_da_dat"]

    conn.close()  # Đóng kết nối

    # Truyền các dữ liệu thống kê vào template
    return render_template('thong_ke.html', tong_doanh_thu=tong_doanh_thu, 
                           so_luong_khach_hang=so_luong_khach_hang, 
                           so_luong_tour_da_dat=so_luong_tour_da_dat)

@app.route('/sua-khach-hang/<int:UserID>', methods=['GET', 'POST'])
def sua_khach_hang(UserID):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        Full_Name = request.form['Full_Name']
        ID_number = request.form['ID_number']
        IdType = request.form['IdType']
        Phone_number = request.form['Phone_number']
        Email = request.form['Email']
        Address = request.form['Address']

        # Cập nhật thông tin khách hàng trong cơ sở dữ liệu
        cursor.execute("""
            UPDATE User 
            SET Full_Name = %s, ID_number = %s, IdType = %s, Phone_number = %s, Email = %s, Address = %s
            WHERE UserID = %s
        """, (Full_Name, ID_number, IdType, Phone_number, Email, Address, UserID))

        conn.commit()
        conn.close()

        return redirect(url_for('quan_ly_khach_hang'))  # Quay lại trang quản lý khách hàng sau khi sửa

    # Lấy thông tin khách hàng hiện tại để hiển thị trong form
    cursor.execute("SELECT * FROM User WHERE UserID = %s", (UserID,))
    khach_hang = cursor.fetchone()

    conn.close()

    return render_template('sua_khach_hang.html', khach_hang=khach_hang)

@app.route('/dat-ve', methods=['GET', 'POST'])
def dat_ve():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        TourID = int(request.form['TourID'])
        UserID = request.form['UserID']
        InvoiceID = request.form['InvoiceID']
        Booking_day = date.today()
        # Lấy giá tour để tính tổng tiền
        cursor.execute("SELECT Price, Num_tickets FROM tour WHERE TourID = %s", (TourID,))
        tours = cursor.fetchone()
        Quantity = tours['Num_tickets']
        Total = tours['Price'] * Quantity
        # Lấy danh sách khách hàng
        cursor.execute("SELECT UserID, Full_Name FROM User")
        khach_hangs = cursor.fetchall()  

        # Thêm dữ liệu vào bảng DatVe
        cursor.execute("""
            INSERT INTO Invoice (InvoiceID, UserID, TourID, Booking_day, Quantity, Total)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (InvoiceID, UserID, TourID, Booking_day, Quantity, Total))
        
        conn.commit()
        conn.close()
        
        # Quay lại trang danh sách hoặc trang quản lý đặt vé
        return redirect(url_for('quan_ly_tour'))

    # Lấy thông tin tour để hiển thị trong form
    cursor.execute("SELECT * FROM Tour ")
    tours = cursor.fetchall()
    cursor.execute("SELECT * FROM User ")
    khach_hangs = cursor.fetchall()
    conn.close()
    
    return render_template('dat_ve.html', tours= tours,khach_hangs=khach_hangs)
if __name__ == '__main__':
    app.run(debug=True)


