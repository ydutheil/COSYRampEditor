#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QRegExpValidator>
#include <QDoubleSpinBox>



class CustomSpinBox : public QDoubleSpinBox {
    Q_OBJECT

public:
    explicit CustomSpinBox(QWidget* parent =0);
    virtual QValidator::State validate(QString & text, int & pos) const;

private:
    QRegExpValidator* validator;

};
#endif // WIDGET_H
